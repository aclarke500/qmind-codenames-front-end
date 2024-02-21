from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import random

app = Flask(__name__)
CORS(app)
@cross_origin(origins='*')


@app.route('/load_board')
def load_board():
  words = [
    "apple", "dog", "river", "book", "sky", "orange", "music", "python", "coffee", "pencil",
    "car", "road", "tree", "mountain", "ocean", "sandwich", "laptop", "glasses", "mouse", "phone",
    "flower", "shirt", "shoe", "house", "light", "water", "cake", "chair", "desk", "guitar",
    "bottle", "key", "clock", "photo", "map", "star", "cloud", "rain", "snow", "sun",
    "moon", "planet", "universe", "forest", "beach", "city", "river", "animal", "bird", "fish"
  ]
  indices = random.sample(range(len(words)), 25)
  word_choices = []
  for i in indices:
      word_choices.append(words[i])

  return jsonify({'words': word_choices, 'hint':'vowels'})


@app.route('/check_word', methods=['POST'])
def check_word():
  data = request.json
  if not data or 'word' not in data:  
      return jsonify({'error': 'No word provided'}), 400
  
  vowels = 'aeiou'
  letters = 'spr'
  return jsonify({'correct' : data['word'][0] in vowels or data['word'][0] in letters})
     

