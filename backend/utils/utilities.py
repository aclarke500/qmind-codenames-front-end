import torch
from torch import Tensor
#import matplotlib.pyplot as plt
import torch.nn.functional as F
from model.spymaster import SentenceEncoder, MORSpyMaster

def get_device(is_cuda: str):
    if (is_cuda.lower() == 'y' and torch.cuda.is_available()):
        return torch.device("cuda")
    return torch.device("cpu")

def convert_args_str_to_bool(arg: str):
    return True if arg.lower() == 'y' else False
 
# def save_loss_plot(losses_train: list, losses_test: list, save_path: str):
#     # Plot training losses
#     plt.plot([i for i in range(len(losses_train))], losses_train, label='Training Loss')
#     plt.plot([i for i in range(len(losses_test))], losses_test, label='Test Loss')
#     # Set labels
#     #plt.title("Training Loss")
#     plt.xlabel("Epoch")
#     plt.ylabel("Loss")

#     # Show the legend
#     plt.legend()

#     # Save the plot
#     plt.savefig(save_path)
#     plt.close()

def calc_game_scores_no_assasin(model_out: Tensor, pos_encs: Tensor, neg_encs: Tensor, neut_encs: Tensor, device: torch.device):
    model_out_expanded = model_out.unsqueeze(1)
    pos_scores = F.cosine_similarity(model_out_expanded, pos_encs, dim=2)
    neg_scores = F.cosine_similarity(model_out_expanded, neg_encs, dim=2)
    neut_scores = F.cosine_similarity(model_out_expanded, neut_encs, dim=2)

    combined_scores = torch.cat((pos_scores, neg_scores, neut_scores), dim=1)
    _, indices = combined_scores.sort(dim=1, descending=True)

    # create reward copies
    pos_reward = torch.zeros(pos_scores.shape[1]).to(device)
    neg_reward = torch.ones(neg_scores.shape[1]).to(device) * 2
    neut_reward = torch.ones(neut_scores.shape[1]).to(device) 

    combined_rewards = torch.cat((pos_reward, neg_reward, neut_reward))
    # Make shape [batch_size, total_number_of_embeddings]
    combined_rewards = combined_rewards.expand((combined_scores.shape[0], combined_rewards.shape[0]))
    # Retrieve the ordered number of rewards, in the order of highest cossine similarity
    rewards = torch.gather(combined_rewards, 1, indices)
    # set all target embeddings to 0 and unwanted embeddings to 1
    non_zero_mask = torch.where(rewards != 0, 1., 0.)
    # Find the total number of correct guesses, equal to the index of the first non-zero value in the mask
    num_correct = torch.argmax(non_zero_mask, dim=1)
    # Find the first incorrect value
    first_incorrect_value = rewards[torch.arange(rewards.size(0)), num_correct]
    return num_correct.float().mean(), first_incorrect_value.mean() - 1

def calc_codenames_score(model_out: Tensor, pos_encs: Tensor, neg_encs: Tensor, neut_encs: Tensor, assas_encs: Tensor, device: torch.device):
    model_out_expanded = model_out.unsqueeze(1)
    assas_expanded = assas_encs.unsqueeze(1)

    pos_scores = F.cosine_similarity(model_out_expanded, pos_encs, dim=2)
    neg_scores = F.cosine_similarity(model_out_expanded, neg_encs, dim=2)
    neut_scores = F.cosine_similarity(model_out_expanded, neut_encs, dim=2)
    assas_scores = F.cosine_similarity(model_out_expanded, assas_expanded, dim=2)

    combined_scores = torch.cat((pos_scores, neg_scores, neut_scores, assas_scores), dim=1)
    _, indices = combined_scores.sort(dim=1, descending=True)

    # create reward copies
    pos_reward = torch.zeros(pos_scores.shape[1]).to(device)
    neg_reward = torch.ones(neg_scores.shape[1]).to(device) * 2
    neut_reward = torch.ones(neut_scores.shape[1]).to(device) 
    assas_reward = torch.ones(assas_scores.shape[1]).to(device) * 3

    combined_rewards = torch.cat((pos_reward, neg_reward, neut_reward, assas_reward))
    # Make shape [batch_size, total_number_of_embeddings]
    combined_rewards = combined_rewards.expand((combined_scores.shape[0], combined_rewards.shape[0]))
    # Retrieve the ordered number of rewards, in the order of highest cosine similarity
    rewards = torch.gather(combined_rewards, 1, indices)
    # set all target embeddings to 0 and unwanted embeddings to 1
    non_zero_mask = torch.where(rewards != 0, 1., 0.)
    # Find the total number of correct guesses, equal to the index of the first non-zero value in the mask
    num_correct = torch.argmax(non_zero_mask, dim=1)
    # Find the first incorrect value
    first_incorrect_value = rewards[torch.arange(rewards.size(0)), num_correct]

    assassin_sum = torch.sum(first_incorrect_value == 3, dim=0)
    neg_sum = torch.sum(first_incorrect_value == 2, dim=0)
    neut_sum = torch.sum(first_incorrect_value == 1, dim=0)

    return num_correct.float().mean(), neg_sum, neut_sum, assassin_sum

def encode_words(model: MORSpyMaster, words: list) -> Tensor:
    embeddings = model.encoder(words)
    return embeddings.to(model.device)

def score_response(words: list, guess_emb: Tensor, targ_embs: Tensor, neg_embs: Tensor, neut_embs: Tensor, assas_emb: Tensor):
    combined_embeddings = torch.cat((targ_embs, neg_embs, neut_embs, assas_emb), dim=0)
    cosine_scores = F.cosine_similarity(guess_emb, combined_embeddings, dim=1)
    cos_scores, cos_indices = cosine_scores.sort(descending=True)

    sorted_words = [words[i] for i in cos_indices]
    return sorted_words, cos_scores


def process_prompt_data(data, model: MORSpyMaster):
    targ_words = data['target_words']
    neg_words = data['negative_words']
    neut_words = data['neutral_words']
    assas_word = data['assassin_word']
    words = targ_words + neg_words + neut_words
    words.append(assas_word)

    targ_embs = encode_words(model, targ_words)
    neg_embs =  encode_words(model, neg_words)
    neut_embs = encode_words(model, neut_words)
    assas_emb = encode_words(model, assas_word)

    with torch.no_grad():
        guess, guess_emb = model(targ_embs, neg_embs, neut_embs, assas_emb)
    
    sorted_words, word_scores = score_response(words, guess_emb, targ_embs, neg_embs, neut_embs, assas_emb)
    return guess, sorted_words, word_scores.tolist()







