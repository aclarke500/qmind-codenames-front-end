from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request
import random
from model.spymaster import MORSpyMaster
from datasets.dataset import CodeNamesDataset
from utils.vector_search import VectorSearch
import utils.utilities as utils
import torch
import torch.nn.functional as F
import json


VOCAB_PATH = "/home/marcuswrrn/Projects/QMIND/qmind-codenames-front-end/backend/data/words_extended.json"
BOARD_PATH = "/home/marcuswrrn/Projects/QMIND/qmind-codenames-front-end/backend/data/codenames_boards.json"
MODEL_PATH = "/home/marcuswrrn/Projects/QMIND/qmind-codenames-front-end/backend/data/model.pth"

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

@app.route('/model', methods=['GET'])
def run_model():
    index = random.randint(0, len(dataset))
    sents, embs = dataset[index]

    pos_sent, neg_sent, neut_sent, assas_sent = sents
    # Process embeddings
    pos_embs, neg_embs, neut_embs, assas_emb = embs
    pos_embs, neg_embs = pos_embs.to(device), neg_embs.to(device)
    neut_embs, assas_emb = neut_embs.to(device), assas_emb.to(device)
    assas_emb = assas_emb.unsqueeze(0)

    with torch.no_grad():
       guess, guess_emb = model(pos_embs, neg_embs, neut_embs, assas_emb)

    words = pos_sent + ' ' + neg_sent + ' ' + neut_sent + ' ' + assas_sent
    words = words.split(' ')

    combined_embeddings = torch.cat((pos_embs, neg_embs, neut_embs, assas_emb), dim=0)
    cosine_scores = F.cosine_similarity(guess_emb, combined_embeddings, dim=1)

    cos_scores, cos_indices = cosine_scores.sort(descending=True)

    sorted_words = [words[i] for i in cos_indices]

    return jsonify({'hint': f'{guess}', 'targets': pos_sent, 'negative': neg_sent, 'neutral': neut_sent, 'assassin': assas_sent, 'similar_words': sorted_words, 'scores': cos_scores.tolist()})

def encode_words(words: list) -> torch.Tensor:
    embeddings = model.encoder(words)
    return embeddings.to(device)

@app.route('/prompt-model', methods=['POST'])
def prompt_model():
    data = request.get_json()
    # TODO: Check viability of data
    # return 'egg'

    cpu_hint, sorted_words, word_scores = utils.process_prompt_data(data, model)
    data_for_human = {
        "target_words": data['negative_words'],
    "negative_words": data['target_words'],
    "neutral_words": ["rabbit", "dog", "boop"],
    "assassin_word": "assassin"
    }

    human_hint, _, _, = utils.process_prompt_data(data_for_human, model)

    return jsonify({'cpu_hint': cpu_hint, 'human_hint':human_hint, 'similar_words': sorted_words, 'scores': word_scores})


if __name__ == "__main__":
   prompt_model()
   app.run(debug=True)
