import os
import numpy as np
import pandas as pd
import joblib
from flask import Flask, jsonify, request
from flask_cors import CORS
from stable_baselines3 import PPO
import logging

# Disable OneDNN optimizations for TensorFlow if needed
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Initialize Flask app and configure CORS
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load circuit data from CSV
def load_circuit_data():
    try:
        df = pd.read_csv('circuits.csv')
        circuit_data = df.set_index('Circuit Name').to_dict('index')
        logging.info("Circuit data loaded successfully.")
        return circuit_data
    except FileNotFoundError:
        logging.error("circuits.csv file not found. Ensure it exists in the script directory.")
    except Exception as e:
        logging.error(f"Error loading circuit data: {str(e)}")
    return {}

circuit_data = load_circuit_data()

@app.route('/api/get_circuit_info', methods=['POST'])
def get_circuit_info():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        return response
    try:
        if not circuit_data:
            return jsonify({'error': 'Circuit data is not available'}), 500
        return jsonify(circuit_data)
    except Exception as e:
        logging.error(f"Error in get_circuit_info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_pit_decision', methods=['POST'])
def get_pit_decision():
    try:
        data = request.get_json()
        logging.debug(f"Input data: {data}")

        # Validate input data
        required_keys = ['tire_wear', 'race_position', 'circuit_name']
        if not all(key in data for key in required_keys):
            return jsonify({'error': 'Missing required parameters'}), 400

        tire_wear = data['tire_wear']
        race_position = data['race_position']
        circuit_name = data['circuit_name']
        weather = data.get('weather', 'clear').lower()
        logging.debug(f"Weather: {weather}")

        if circuit_name not in circuit_data:
            return jsonify({'error': 'Circuit not found'}), 404

        circuit_info = circuit_data[circuit_name]
        track_length = circuit_info['Track Length (km)'] * 1000  # Convert to meters
        logging.debug(f"Circuit info: {circuit_info}, Track length: {track_length}")

        # Load the reinforcement learning model
        try:
            model = PPO.load('reinforcement_learning_model.h5')
            logging.debug("Model loaded successfully.")
        except FileNotFoundError:
            logging.error("Reinforcement learning model file not found.")
            return jsonify({'error': 'Model file not found'}), 500
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            return jsonify({'error': 'Error loading model'}), 500

        # Prepare data for prediction
        observation = np.array([tire_wear, race_position, track_length])
        logging.debug(f"Observation shape: {observation.shape}")

        # Reshape observation if required
        observation = observation.reshape(1, -1)
        logging.debug(f"Reshaped observation: {observation}")

        # Get action from the model
        try:
            action, _states = model.predict(observation, deterministic=True)
            logging.debug(f"Action returned: {action}")
        except Exception as e:
            logging.error(f"Error during model prediction: {str(e)}")
            return jsonify({'error': 'Error during model prediction'}), 500
        # Adjust pit threshold based on weather
        base_threshold = 85
        pit_threshold = base_threshold * 1.2 if weather == 'rain' else base_threshold
        logging.debug(f"Pit threshold: {pit_threshold}")

        pit_decision = "Pit" if action[0] > pit_threshold else "No Pit"

        return jsonify({
            'action': action[0],
            'pit_decision': pit_decision,
            'circuit': circuit_name,
            'track_type': circuit_info['Track Type'],
            'average_wear_rate': circuit_info['Average Wear Rate']
        })
    except Exception as e:
        logging.error(f"Error in get_pit_decision: {str(e)}")
        return jsonify({'error': 'Failed to get pit stop decision. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
