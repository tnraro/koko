from sentence_transformers import SentenceTransformer, util
from torch import Tensor

tensorByWord: dict[str, Tensor] = {}

def embedding(model: SentenceTransformer, s: str | list[str]) -> Tensor:
  if (isinstance(s, str)):
    if s in tensorByWord:
      return tensorByWord[s]
    else:
      tensor = model.encode(s, convert_to_tensor=True)
      tensorByWord[s] = tensor
      return tensor
  elif (isinstance(s, list)):
    # TODO: caching
    tensor = model.encode(s, convert_to_tensor=True)
    for i, a in enumerate(s):
      tensorByWord[a] = tensor[i]
    return tensor
  
  
def similarity(model: SentenceTransformer, answerTensor: Tensor, s: str):
  tensor = embedding(model, s)
  similarity = util.pytorch_cos_sim(answerTensor, tensor)[0, 0].item()
  return similarity