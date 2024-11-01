# rl_agent.py
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from environment import RaceEnvironment

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class PitStopAgent:
    def __init__(self, state_size, action_size, env):
        self.env = env
        self.model = DQN(state_size, action_size)
        self.target_model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.replay_buffer = []
        self.batch_size = 64

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(0, 2)  # Chọn ngẫu nhiên giữa 0 và 1
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        actions = self.model(state_tensor)
        return torch.argmax(actions).item()

    def train(self, episodes=1000):
        for episode in range(episodes):
            state = self.env.reset()
            done = False
            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.replay_buffer.append((state, action, reward, next_state, done))
                self.update_model()
                state = next_state
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

    def update_model(self):
        if len(self.replay_buffer) < self.batch_size:
            return
        batch = np.random.choice(self.replay_buffer, self.batch_size, replace=False)
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
                target = reward + self.gamma * torch.max(self.target_model(next_state_tensor)).item()
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.model(state_tensor)
            q_value = q_values[0][action]
            loss = (q_value - target) ** 2
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
