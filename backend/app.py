from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from rl_agent import PitStopAgent
from environment import RaceEnvironment

app = Flask(__name__)
CORS(app)

# Khởi tạo môi trường đua và tác tử RL
env = RaceEnvironment(track_conditions={'wear_rate': 0.01, 'base_time': 75})
agent = PitStopAgent(state_size=3, action_size=2, env=env)

# Route cho trang chủ để phục vụ file index.html từ thư mục 'frontend'
@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

# Endpoint cho huấn luyện tác tử RL
@app.route('/train', methods=['POST'])
def train():
    data = request.json
    episodes = data.get("episodes", 1000)
    agent.train(episodes)
    return jsonify({"status": "Training completed"})

# Endpoint dự đoán quyết định pit stop
@app.route('/predict', methods=['POST'])
def predict():
    state = request.json.get('state', [])
    action = agent.choose_action(state)
    return jsonify({"action": action})

if __name__ == '__main__':
    app.run(debug=True)
