from environment import F1Environment
from models.dqn_agent import DQNAgent
import numpy as np
import time
from datetime import datetime

def train_model(
    episodes=100,  
    max_steps=200,  
    batch_size=32,
    min_epsilon=0.01,
    save_interval=10
):
    env = F1Environment()
    agent = DQNAgent()
    
    # Track metrics
    rewards_history = []
    epsilon_history = []
    start_time = time.time()
    best_reward = float('-inf')
    
    print("Training started...")
    
    for episode in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, 4])
        total_reward = 0
        
        for step in range(max_steps):
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = np.reshape(next_state, [1, 4])
            
            agent.train(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            
            if done:
                break
        
        # Save metrics
        rewards_history.append(total_reward)
        epsilon_history.append(agent.epsilon)
        
        # Progress tracking
        if episode % 5 == 0:
            elapsed = time.time() - start_time
            avg_reward = np.mean(rewards_history[-5:])
            print(f"Episode: {episode}/{episodes} | "
                  f"Reward: {total_reward:.2f} | "
                  f"Epsilon: {agent.epsilon:.2f} | "
                  f"Time: {elapsed:.2f}s")
        
        # Save checkpoint if better
        if total_reward > best_reward:
            best_reward = total_reward
            agent.model.save('best_model.h5')
        
        # Early stopping
        if agent.epsilon <= min_epsilon:
            print("Early stopping: epsilon reached minimum")
            break
        
        # Regular checkpoint
        if episode % save_interval == 0:
            agent.model.save(f'model_checkpoint_{episode}.h5')
    
    # Save final model
    final_time = time.time() - start_time
    print(f"\nTraining completed in {final_time:.2f} seconds")
    agent.model.save('reinforcement_learning_model.h5')
    
    return rewards_history, epsilon_history

if __name__ == "__main__":
    train_model()