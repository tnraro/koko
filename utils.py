def scoreIndicator(score: float):
  n = round(score * 10)
  return ("🟩" * max(0, int(n / 2))) + ("" if n % 2 == 0 else "🟨")