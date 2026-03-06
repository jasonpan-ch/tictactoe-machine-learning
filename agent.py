import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
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
        self.epsilon_decay = 0.9997
        self.epsilon_min = 0.01
        self.memory = deque(maxlen = 10000)
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
        
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(np.array(states))
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(np.array(next_states))
        dones = torch.FloatTensor(dones).unsqueeze(1)

        current_q_values = self.model(states).gather(1, actions)
        next_q_values = self.model(next_states).max(1)[0].unsqueeze(1)
        target_q_values = rewards + (self.gamma * next_q_values * (1 - dones))

        loss = self.criterion(current_q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay