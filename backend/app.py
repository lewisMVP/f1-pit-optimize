# app.py
from flask import Flask, request, jsonify
from rl_agent import PitStopAgent
from environment import RaceEnvironment

app = Flask(__name__)
env = RaceEnvironment(track_conditions={'wear_rate': 0.01, 'base_time': 75})
agent = PitStopAgent(state_size=3, action_size=2, env=env)

@app.route('/train', methods=['POST'])
def train():
    data = request.json
    episodes = data.get("episodes", 1000)
    agent.train(episodes)
    return jsonify({"status": "Training completed"})

@app.route('/predict', methods=['POST'])
def predict():
    state = request.json['state']
    action = agent.choose_action(state)
    return jsonify({"action": action})

if __name__ == '__main__':
    app.run(debug=True)
