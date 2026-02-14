import torch
import torch.optim as optim
import torch.nn as nn
import random

from neural_network import DQN
from collections import deque

class Agent:
    def __init__(self, learning_rate = 0.001, gamma = 0.9, epsilon = 1.0):
        self.model = DQN()
        self.optimizer = optim.Adam(self.model.parameters(), lr = learning_rate)
        self.criterion = nn.MSELoss()
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = 0.99995
        self.epsilon_min = 0.01
        self.memory = deque(maxlen = 2000)
        self.batch_size = 32

    def select_action(self, state, legal_moves):
        if random.random() < self.epsilon:
            return random.choice(legal_moves)
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        q_values = q_values.detach().numpy()[0]
        legal_q_values = {move: q_values[move] for move in legal_moves}
        best_move = max(legal_q_values, key=legal_q_values.get)
        return best_move
    
    def store_experience(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in batch:
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
            current_q = self.model(state_tensor)[0][action]
            if done:
                target_q = torch.tensor(float(reward))
            else:
                next_q_values = self.model(next_state_tensor)
                target_q = reward + self.gamma * torch.max(next_q_values)
            loss = self.criterion(current_q, target_q)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay