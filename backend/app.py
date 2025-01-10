import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, jsonify, request
import pandas as pd
import joblib
from flask_cors import CORS

# Add necessary imports for reinforcement learning
import numpy as np
from stable_baselines3 import PPO

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

# Load circuit data from CSV
def load_circuit_data():
    try:
        df = pd.read_csv('circuits.csv')
        circuit_data = df.set_index('Circuit Name').to_dict('index')
        return circuit_data
    except Exception as e:
        print(f"Error loading circuit data: {str(e)}")
        return {}

circuit_data = load_circuit_data()

@app.route('/api/get_circuit_info', methods=['POST'])
def get_circuit_info():
    try:
        return jsonify(circuit_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_pit_decision', methods=['POST'])
def get_pit_decision():
    try:
        data = request.get_json()
        tire_wear = data['tire_wear']
        race_position = data['race_position']
        circuit_name = data['circuit_name']
        weather = data.get('weather', 'clear')

        if circuit_name not in circuit_data:
            return jsonify({'error': 'Circuit not found'}), 404
            
        circuit_info = circuit_data[circuit_name]
        track_length = circuit_info['Track Length (km)'] * 1000

        # Load the reinforcement learning model
        model = PPO.load('reinforcement_learning_model.zip')
        
        # Prepare data for prediction
        observation = np.array([tire_wear, race_position, track_length])

        # Get the action (pit decision) from the model
        action, _states = model.predict(observation, deterministic=True)
        
        # Adjust pit threshold based on weather
        base_threshold = 85
        pit_threshold = base_threshold * 1.2 if weather == 'rain' else base_threshold
        
        pit_decision = "Pit" if action[0] > pit_threshold else "No Pit"

        return jsonify({
            'action': action[0],
            'pit_decision': pit_decision,
            'circuit': circuit_name,
            'track_type': circuit_info['Track Type'],
            'average_wear_rate': circuit_info['Average Wear Rate']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)