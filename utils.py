import math

def scoreIndicator(score: float):
  n = round(score * 10)
  pos = n > 0
  return (("🟩" if pos else "🟥") * max(0, abs(math.trunc(n / 2)))) + ("" if n % 2 == 0 else ("🟨" if pos else "🟧"))
