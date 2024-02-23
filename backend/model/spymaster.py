import torch
from torch._C import device
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor, device
#from transformers import DebertaConfig, DebertaModel, DebertaTokenizer
from utils.vector_search import VectorSearch
from sentence_transformers import SentenceTransformer


class SentenceEncoder(nn.Module):
    def __init__(self, model_name='all-mpnet-base-v2'):
        super(SentenceEncoder, self).__init__()

        self.name = model_name
        self.encoder = SentenceTransformer(self.name)

    def forward(self, text: torch.Tensor):
        encodings = self.encoder.encode(text, convert_to_tensor=True)
        if encodings.ndim == 1:
            encodings = encodings.unsqueeze(0)
        # out = self.fc(encodings)
        return encodings

class MORSpyMaster(nn.Module):
    """
    Multi-Objective Retrieval model for codenames with 4 competing objectives
    """
    def __init__(self, vocab: VectorSearch, device: torch.device, neutral_weight=1.0, negative_weight=0.0, assas_weights=-10.0, backbone='all-mpnet-base-v2', vocab_size=80, search_pruning=False):
        super().__init__()
        self.encoder = SentenceEncoder(backbone)
        self.vocab_size = vocab_size

        self.neut_weight = neutral_weight
        self.neg_weight = negative_weight
        self.assas_weights = assas_weights
        
        self.fc = nn.Sequential(
            nn.Linear(3072, 2304),
            nn.Tanh(),
            nn.Linear(2304, 1700),
            nn.Tanh(),
            nn.Linear(1700, 1000),
            nn.Tanh(),
            nn.Linear(1000, 768),
        )
        self.vocab = vocab
        self.device = device

        self.search_pruning = search_pruning

    def _process_embeddings(self, embs: Tensor):
        """Mean pool and normalize all embeddings"""
        out = torch.mean(embs, dim=1)
        out = F.normalize(out, p=2, dim=1)
        return out
    
    def _expand_encodings_for_search(self, encs: Tensor):
        """Converts shape input encodings from [batch_size, num_encodings, embedding_size] -> [batch_size, vocab_size, num_encodings, embedding_size]"""
        return encs.unsqueeze(1).expand(-1, self.vocab_size, -1, -1)
    
    def _get_primary_reward(self, pos_scores: Tensor, neg_scores: Tensor, neut_scores: Tensor, assas_scores: Tensor, reverse=False):
        combined_scores = torch.cat((pos_scores, neg_scores, neut_scores, assas_scores), dim=2)
        _, indices = combined_scores.sort(dim=2, descending=True)

        # Create reward copies
        pos_reward = torch.zeros(pos_scores.shape[2]).to(self.device)   # Positive must be the only zero value
        neg_reward = torch.ones(neg_scores.shape[2]).to(self.device)
        neut_reward = torch.ones(neut_scores.shape[2]).to(self.device) 
        assas_reward = torch.ones(assas_scores.shape[2]).to(self.device)

        combined_rewards = torch.cat((pos_reward, neg_reward, neut_reward, assas_reward))
        combined_rewards = combined_rewards.expand((combined_scores.shape[0], self.vocab_size, combined_rewards.shape[0]))
        # Map rewards to their corresponding indices
        rewards = torch.gather(combined_rewards, 2, indices)

        # Find the total number of correct guesses, equal to the index of the first non-zero value
        num_correct = torch.argmax(rewards, dim=2)

        if reverse:
            # Find the inverse of the positive reward (num incorrect)
            return (pos_reward.shape[0] - num_correct)
        
        return num_correct 

    def _get_reward_tensor(self, size: int, weight: float, reverse: bool) -> Tensor:
        reward = torch.ones(size).to(self.device) * weight
        if reverse:
            return reward * -1
        return reward

    def _get_secondary_reward(self, neg_scores: Tensor, neut_scores: Tensor, assas_scores: Tensor, reverse=False):
        """Finds the highest value between both the negative, neutral and assassin scores"""
        combined = torch.cat((neg_scores, neut_scores, assas_scores), dim=2)
        _, indices = combined.sort(dim=2, descending=True)

        neg_reward = self._get_reward_tensor(neg_scores.shape[2], self.neg_weight, reverse)
        neut_reward = self._get_reward_tensor(neut_scores.shape[2], self.neut_weight, reverse)
        assas_reward = self._get_reward_tensor(assas_scores.shape[2], self.assas_weights, reverse)

        combined_rewards = torch.cat((neg_reward, neut_reward, assas_reward))
        combined_rewards = combined_rewards.expand((combined.shape[0], self.vocab_size, combined_rewards.shape[0]))
        rewards = torch.gather(combined_rewards, 2, indices)

        # Find the values of the first index, equal to the given reward (score of the most similar unwanted embedding)
        # Due to the sequential nature of codenames only the first non-target guess matters
        reward = rewards[:, :, 0]
        return reward


    def _get_total_reward(self, word_encs: Tensor, pos_encs: Tensor, neg_encs: Tensor, neut_encs: Tensor, assas_encs: Tensor, reverse: bool) -> Tensor:
        # Find scores
        pos_scores = F.cosine_similarity(word_encs, pos_encs, dim=3)
        neg_scores = F.cosine_similarity(word_encs, neg_encs, dim=3)
        neut_scores = F.cosine_similarity(word_encs, neut_encs, dim=3)
        assas_scores = F.cosine_similarity(word_encs, assas_encs, dim=3)
        # Get reward
        primary_reward = self._get_primary_reward(pos_scores, neg_scores, neut_scores, assas_scores, reverse=reverse)
        secondary_reward = self._get_secondary_reward(neg_scores, neut_scores, assas_scores, reverse=reverse)

        return primary_reward + secondary_reward
    
    def _find_scored_embeddings(self, reward, word_embeddings):
        # Find lowest scoring and highest scored indices
        index_max_vals, index_max = torch.topk(reward, k=word_embeddings.shape[1]//2, dim=1)
        index_min_vals, index_min = torch.topk(reward, k=word_embeddings.shape[1]//2, largest=False, dim=1)

        embeddings_max = torch.gather(word_embeddings, 1, index_max.unsqueeze(-1).expand(-1, -1, word_embeddings.shape[2]))
        embeddings_min = torch.gather(word_embeddings, 1, index_min.unsqueeze(-1).expand(-1, -1, word_embeddings.shape[2]))

        max_embeddings_pooled = self._process_embeddings(embeddings_max)
        min_embeddings_pooled = self._process_embeddings(embeddings_min)

        # Highest scoring word embedding
        highest_scoring_embedding = embeddings_max[:, 0]
        highest_scoring_embedding_index = index_max[:, 0]

        return highest_scoring_embedding, highest_scoring_embedding_index, max_embeddings_pooled, min_embeddings_pooled

    def find_search_embeddings(self, word_embeddings: Tensor, pos_encs: Tensor, neg_encs: Tensor, neut_encs: Tensor, assassin_encs: Tensor):
        word_embs_expanded = word_embeddings.unsqueeze(2)
        # Process encoding shapes
        pos_encs = self._expand_encodings_for_search(pos_encs)
        neg_encs = self._expand_encodings_for_search(neg_encs)
        neut_encs = self._expand_encodings_for_search(neut_encs)
        assas_encs = self._expand_encodings_for_search(assassin_encs.unsqueeze(1))

        tot_reward = self._get_total_reward(word_embs_expanded, pos_encs, neg_encs, neut_encs, assas_encs, reverse=False)

        return self._find_scored_embeddings(tot_reward, word_embeddings)

    def _get_combined_input(self, pos_embs: Tensor, neg_embs: Tensor, neut_embs: Tensor, assas_emb: Tensor) -> Tensor:
        neg_emb = self._process_embeddings(neg_embs)
        neut_emb = self._process_embeddings(neut_embs)
        pos_emb = self._process_embeddings(pos_embs)

        return torch.cat((neg_emb, assas_emb, neut_emb, pos_emb), dim=1)
    
    def _convert_word_embeddings_to_tensor(self, embs: Tensor):
        return torch.tensor(embs).to(self.device).squeeze(1)

    def forward(self, pos_embs: Tensor, neg_embs: Tensor, neut_embs: Tensor, assas_emb: Tensor):
        if not self.training:
            pos_embs, neg_embs, neut_embs = pos_embs.unsqueeze(0), neg_embs.unsqueeze(0), neut_embs.unsqueeze(0)
        concatenated = self._get_combined_input(pos_embs, neg_embs, neut_embs, assas_emb)
        model_out = self.fc(concatenated)

        model_out = F.normalize(model_out, p=2, dim=1)

        # ANN Search
        words, word_embeddings, dist = self.vocab.search(model_out, num_results=self.vocab_size)
        word_embeddings = self._convert_word_embeddings_to_tensor(word_embeddings)

        if self.search_pruning:
            self._prune_word_embeddings(word_embeddings, model_out)

        search_embedding, search_out_index, search_out_max, search_out_min = self.find_search_embeddings(word_embeddings, pos_embs, neg_embs, neut_embs, assas_emb)
        search_word = words[0][search_out_index]

        if self.training:
            return model_out, search_embedding, search_out_max, search_out_min
        
        return search_word, search_embedding
