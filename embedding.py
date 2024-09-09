from sentence_transformers import SentenceTransformer
import db

def embedding(model: SentenceTransformer, word: str):
  e = db.selectWordEmbedding(word)
  if e != None:
    return e[1]
  else:
    embedding = model.encode(word)
    db.insertWordEmbedding(word, embedding)
    return embedding

def prepare(model: SentenceTransformer):
  words = db.selectWordsWithoutEmbedding()
  if len(words) == 0:
    return
  embeddings = model.encode(words)
  db.dropVssIndices()
  db.insertWordEmbeddings([(word, embeddings[i]) for i, word in enumerate(words)])
  db.createVssIndices()
  
def similarity(model: SentenceTransformer, a: str, b: str):
  embedding(model, a)
  embedding(model, b)
  return db.similarity(a, b)

def guess(model: SentenceTransformer, answer: str, guess: str):
  embedding(model, answer)
  embedding(model, guess)
  return db.guess(answer, guess)