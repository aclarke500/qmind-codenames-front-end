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

  return jsonify({'words': word_choices})




@app.route('/verify', methods=['POST'])
def verify():
  data = request.json
  if not data or 'words' not in data:  # Check for 'words' instead of 'text'
      return jsonify({'error': 'No words provided'}), 400
  
  # Proceed with the original logic
  valid_words = []
  bust_words = []
  words = data['words']  # Access the words correctly
  vowels = 'aeiou'
  for w in words:
     if w[0] in vowels:
        valid_words.append(w)
     else:
        bust_words.append(w)


  return jsonify({'all_words': words, 'valid_words': valid_words, 'bust_words':bust_words})

