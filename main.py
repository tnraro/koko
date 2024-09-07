from sentence_transformers import SentenceTransformer
import json
import random
from embedding import embedding, similarity
from utils import scoreIndicator

with open("data.json") as data:
  words: list[str] = json.load(data)

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
e = embedding(model, words)

needTutorial = True

while True:
  answerIndex = random.randint(0, len(words) - 1)
  answer = words[answerIndex]
  answerTensor = e[answerIndex]

  score = {}

  for word in words:
    s = similarity(model, answerTensor, word)
    score[word] = s

  sortedWords = sorted(words, key=lambda x: score[x], reverse=True)

  print("\n새 놀이가 준비되었어요!")
  if needTutorial:
    print("[귀띔] 단어를 입력하거나 /도움을 입력해보세요!")
    needTutorial = False
  count = 0
  closestRanking = 10000
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
    s = similarity(model, answerTensor, guess)
    if guess in sortedWords:
      ranking = sortedWords.index(guess) + 1
      if ranking < closestRanking:
        closestRanking = ranking
      print(f"{guess}\t{ranking:>4}위\t{scoreIndicator(s)}")
    else:
      print(f"{guess}\t ???위\t{scoreIndicator(s)}")
    if (guess == answer):
      print(str(count) + "회 만에 맞췄어요🥳")
      break
    else:
      if count == 10 and closestRanking > 1000:
        print("[귀띔] 1000위 단어:", sortedWords[999])
      elif count == 100 and closestRanking > 100:
        print("[귀띔] 100위 단어:", sortedWords[99])
      elif count == 1000 and closestRanking > 10:
        print("[귀띔] 10위 단어:", sortedWords[9])