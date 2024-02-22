from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify
import random
import numpy as np
from model.spymaster import MORSpyMaster
from datasets.dataset import CodeNamesDataset
from utils.vector_search import VectorSearch
import torch
from torch.utils.data import DataLoader
import random

VOCAB_PATH = "./data/words_extended.json"
BOARD_PATH = "./data/codenames_boards.json"
MODEL_PATH = "./data/model.pth"

device = torch.device('cuda') if torch.cuda.is_available() else 'cpu'
print(f"Server Running on: {device}")

print(f"Loading embedding data")
dataset = CodeNamesDataset(code_dir=VOCAB_PATH, game_dir=BOARD_PATH)
vocab_data = VectorSearch(dataset, prune=True)

print(f"Loading Model")
model = MORSpyMaster(vocab_data, device=device)

pretrained_dict = None 
if torch.cuda.is_available():
  pretrained_dict = torch.load(MODEL_PATH)   
else: 
   pretrained_dict = torch.load(MODEL_PATH, map_location=torch.device('cpu'))

model.load_state_dict(pretrained_dict)
model.to(device)
model.eval()

print(f"Starting Server")
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


@app.route('/model', methods=['GET'])
def run_model():
    index = random.randint(0, len(dataset))
    sents, embs = dataset[index]

    pos_sent, neg_sent, neut_sent, assas_sent = sents
    # Process embeddings
    pos_embs, neg_embs, neut_embs, assas_emb = embs
    pos_embs, neg_embs = pos_embs.to(device), neg_embs.to(device)
    neut_embs, assas_emb = neut_embs.to(device), assas_emb.to(device)

    with torch.no_grad():
       search_index = model(pos_embs, neg_embs, neut_embs, assas_emb)

    guess = vocab_data.vocab_words[search_index]


    return jsonify({'message': f'{guess}', 'targets': pos_sent, 'negative': neg_sent, 'neutral': neut_sent, 'assassin': assas_sent})


if __name__ == "__main__":
   app.run(debug=True)
