from environment import F1Environment
from models.dqn_agent import DQNAgent
import numpy as np
import time
import json
import os

def train_model(
    episodes=100,
    max_steps=200,
    batch_size=32,
    min_epsilon=0.01,
    save_interval=10
):
    env = F1Environment()
    agent = DQNAgent()
    
    # Create output directory
    os.makedirs('models', exist_ok=True)
    
    # Track metrics
    rewards_history = []
    epsilon_history = []
    start_time = time.time()
    best_reward = float('-inf')
    
    try:
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
            rewards_history.append(float(total_reward))
            epsilon_history.append(float(agent.epsilon))
            
            # Progress tracking
            if episode % 5 == 0:
                print(f"Episode: {episode}/{episodes} | Reward: {total_reward:.2f}")
            
            # Save checkpoint
            if episode % save_interval == 0:
                agent.model.save(f'models/model_checkpoint_{episode}.keras')
        
        # Save final model and metrics
        agent.model.save('models/reinforcement_learning_model.keras')
        
        # Save training metrics
        metrics = {
            'rewards': rewards_history,
            'epsilon': epsilon_history,
            'training_time': time.time() - start_time
        }
        with open('models/training_metrics.json', 'w') as f:
            json.dump(metrics, f)
            
        print(f"Training completed in {time.time() - start_time:.2f} seconds")
        return metrics
        
    except KeyboardInterrupt:
        print("\nTraining interrupted. Saving checkpoint...")
        agent.model.save('models/model_interrupted.keras')
        raise
    except Exception as e:
        print(f"Error during training: {e}")
        raise

if __name__ == "__main__":
    train_model()