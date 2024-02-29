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

VOCAB_PATH ="/Users/adamclarke/Desktop/QMIND/repos/front-end/backend/data/words_extended.json"
BOARD_PATH = "/Users/adamclarke/Desktop/QMIND/repos/front-end/backend/data/codenames_boards.json"
MODEL_PATH = "/Users/adamclarke/Desktop/QMIND/repos/front-end/backend/data/model.pth"


# VOCAB_PATH = "./data/words_extended.json"
# BOARD_PATH = "./data/codenames_boards.json"
# MODEL_PATH = "./data/model.pth"

# score will be updated on front end
worden_wins = 0
player_wins = 0

device = torch.device('cuda') if torch.cuda.is_available() else 'cpu'
print(f"Server Running on: {device}")

print(f"Loading embedding data")
dataset = CodeNamesDataset(code_dir=VOCAB_PATH, game_dir=BOARD_PATH)
vocab_data = VectorSearch(dataset, prune=True)

model = MORSpyMaster(vocab_data, device=device)

pretrained_dict = None 
if torch.cuda.is_available():
  pretrained_dict = torch.load(MODEL_PATH)   
else: 
   pretrained_dict = torch.load(MODEL_PATH, map_location=torch.device('cpu'))

model.load_state_dict(pretrained_dict)
model.to(device)
model.eval()