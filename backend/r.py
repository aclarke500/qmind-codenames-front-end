'''
This is for messing around with the encoder outside
the Flask API
'''
from sentence_transformers import SentenceTransformer
import numpy as np
import random

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))



def guess_words(data):
  model_prediction = []
  hint_vector = model.encode(data['hint'])
  print(hint_vector)

  for w in data['words']:
    word_vector = model.encode(w)
    model_prediction.append([w, 5])

  guesses = []
  indices = random.sample(range(len(data['words'])),len(data['words']))

  for i in indices:
    guesses.append(data['words'][i])

  return ({'guesses':guesses})

def load_board():
  team_one_words = ['python', 'cornsake', 'lizards']
  team_two_words = ['guitar', 'drum', 'bass']
  neutral_words = ['hotdog', 'rock']
  assassin_word = ['shit']

  return {
     'teamOneWords':team_one_words,
     'teamTwoWords':team_two_words,
     'bystanderWords':neutral_words,
     'assassinWord':assassin_word
  }

print(load_board())



data = {
  'words':['hello', 'goodbye', 'beatles'],
  'hint':'music'
}

guess_words(data)
