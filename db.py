import duckdb

con = duckdb.connect("data.duckdb")
con.install_extension("vss")
con.load_extension("vss")

con.execute("drop table words; create table words as from 'words.csv'")
con.execute("""
create table if not exists word_embeddings (
  word varchar primary key,
  embedding float[768] not null
)
""")
con.execute("set hnsw_enable_experimental_persistence = true")

def selectWords():
  return [x[0] for x in con.execute("select * from words").fetchall()]

def hasWord(word: str):
  return con.execute("select * from words where word = ?", [word]).fetchone() is None

def selectWordsWithoutEmbedding():
  return [x[0] for x in con.execute("""
    select words.word
    from words
    left outer join word_embeddings on words.word = word_embeddings.word
    where word_embeddings.word is null
  """).fetchall()]

def insertWordEmbeddings(values: list[tuple[str, any]]):
  return con.executemany("insert or ignore into word_embeddings (word, embedding) values (?, ?)", values)

def insertWordEmbedding(word: str, embedding: any):
  return con.execute("insert into word_embeddings (word, embedding) values (?, ?)", [word, embedding])

def selectWordEmbeddings():
  return con.execute("select * from word_embeddings").fetchall()

def selectWordEmbedding(word: str):
  return con.execute("select * from word_embeddings where word = ?", [word]).fetchone()

def dropVssIndices():
  con.execute("drop index idx")
  con.execute("drop index cos_idx")

def createVssIndices():
  con.execute("create index idx on word_embeddings using hnsw (embedding)")
  con.execute("create index cos_idx on word_embeddings using hnsw (embedding) with (metric = 'cosine')")

def similarity(a: str, b: str):
  return con.execute("""
    select array_cosine_similarity(
      (select embedding from word_embeddings where word = ?),
      (select embedding from word_embeddings where word = ?)
    )
  """, [a, b]).fetchone()[0]

def getSimilarWords(answer: str):
  return [x[0] for x in con.execute(f"""
    select r0.word, (array_cosine_similarity(r0.embedding, answer.embedding)) as similarity
    from
      (select * from words join word_embeddings on words.word = word_embeddings.word) as r0,
      (select embedding from word_embeddings where word=?) as answer
    order by similarity desc
  """, [answer]).fetchall()]

def getNthSimilarWord(answer: str, rank: int):
  return con.execute("""
    with
      word_pool as (from words join word_embeddings on words.word = word_embeddings.word),
      answer as materialized (from word_embeddings select embedding where word = ?)
    from word_pool, answer
    select word_pool.word, (array_cosine_similarity(word_pool.embedding, answer.embedding)) as similarity
    order by similarity desc
    offset ?
    limit 1
  """, [answer, rank - 1]).fetchone()[0]

def guess(answer: str, guess: str):
  return con.execute("""
    with
      word_pool as (from words join word_embeddings on words.word = word_embeddings.word),
      answer as materialized (from word_embeddings select embedding where word = $answer),
      tmp_sorted_word_pool as (
        from word_pool, answer
        select
          word_pool.word,
          (array_cosine_similarity(word_pool.embedding, answer.embedding)) as similarity
      ),
      sorted_word_pool as (
        from tmp_sorted_word_pool
        select 
          row_number() over(order by similarity desc) as rank,
          *
      ),
      guess as (
        from word_embeddings, answer
        select
          word,
          (array_cosine_similarity(word_embeddings.embedding, answer.embedding)) as similarity
        where word = $guess
      ),
      result as (from sorted_word_pool union by name from guess)
    from result
    where word = $guess
    order by rank
    limit 1
  """, {
    "answer": answer,
    "guess": guess,
  }).fetchone()
