from environment import F1Environment
from models.dqn_agent import DQNAgent
import numpy as np

def train_model(episodes=1000):
    env = F1Environment()
    agent = DQNAgent()
    
    for episode in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, 4])
        
        for time in range(500):
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = np.reshape(next_state, [1, 4])
            
            agent.train(state, action, reward, next_state, done)
            state = next_state
            
            if done:
                print(f"Episode: {episode}/{episodes}, Time: {time}")
                break
    
    agent.model.save('reinformcement_learning_model.zip')

if __name__ == "__main__":
    train_model()