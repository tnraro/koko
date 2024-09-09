from sentence_transformers import SentenceTransformer
import random
import db
import embedding
from utils import scoreIndicator

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
embedding.prepare(model)

needTutorial = True

while True:
  words = db.selectWords()
  answerIndex = random.randint(0, len(words) - 1)
  answer = words[answerIndex]

  print("\n새 놀이가 준비되었어요!")
  if needTutorial:
    print("[귀띔] 단어를 입력하거나 /도움을 입력해보세요!")
    needTutorial = False
  count = 0
  closestRank = 10000
  while True:
    guess = input("단어를 입력하세요: ")
    if guess.startswith("/"):
      if (guess == "/포기"):
        print(f"포기했어요😢 정답은~ \"{answer}\"")
        break
      elif (guess == "/종료"):
        print("놀이 끝~ 다음에 또 만나요!")
        exit()
      else:
        print("/도움 /포기 /종료")
      continue
    count += 1
    result = embedding.guess(model, answer, guess)
    print (result)

    if result is not None:
      rank, name, s = result
      if rank is not None:
        print(f"{guess}\t{rank:>4}위\t{scoreIndicator(s)}")
        if rank < closestRank:
          closestRank = rank
      else:
        print(f"{guess}\t ???위\t{scoreIndicator(s)}")
    else:
      v = embedding.similarity(model, answer, guess)
      print(f"{guess}\t ???위\t{scoreIndicator(v)}")
    if (guess == answer):
      print(str(count) + "회 만에 맞췄어요🥳")
      break
    else:
      if count == 10 and closestRank > 1000:
        print("[귀띔] 1000위 단어:", db.getNthSimilarWord(answer, 1000))
      elif count == 100 and closestRank > 100:
        print("[귀띔] 100위 단어:", db.getNthSimilarWord(answer, 100))
      elif count == 1000 and closestRank > 10:
        print("[귀띔] 10위 단어:", db.getNthSimilarWord(answer, 10))