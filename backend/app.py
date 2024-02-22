from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import random
import numpy as np

# model = SentenceTransformer('all-MiniLM-L6-v2')

app = Flask(__name__)
words = {}

CORS(app)
@cross_origin(origins='*')


def dot_product(v1, v2):
    return sum(x*y for x, y in zip(v1, v2))

def norm(v):
    return sum(x*x for x in v) ** 0.5

def cosine_similarity(v1, v2):
    return dot_product(v1, v2) / (norm(v1) * norm(v2))

@app.route('/get_hints', methods=['POST'])
def get_hints():
  data = request.json
  if not data or not 'words' in data or not 'hint' in data:
    return jsonify({'error':'bad inpit'}), 400
  
  # replace with model
  return jsonify({ 
     'hintOne':'reptiles',
     'hintTwo':'binary'
  })

@app.route('/guess_words', methods=['POST'])
def guess_words():
  data = request.json
  if not data or not 'words' in data or not 'hint' in data:
    return jsonify({'error':'bad inpit'}), 400
  
  # replace with model

  guesses = []
  indices = random.sample(range(len(data['words'])),len(data['words']))

  for i in indices:
    guesses.append(data['words'][i])

  return jsonify({'guesses':guesses})

@app.route('/load_board', methods=['GET'])
def load_board():
  team_one_words = ['python', 'cornsake', 'lizards']
  team_two_words = ['guitar', 'drum', 'bass']
  neutral_words = ['hotdog', 'rock']
  assassin_word = ['shit']

  return jsonify({
     'teamOneWords':team_one_words,
     'teamTwoWords':team_two_words,
     'bystanderWords':neutral_words,
     'assassinWord':assassin_word
  })
