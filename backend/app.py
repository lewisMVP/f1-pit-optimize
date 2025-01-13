from flask import Flask, jsonify, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

# Load circuit data from CSV
def load_circuit_data():
    try:
        # Read the CSV file containing circuit information
        df = pd.read_csv('circuitt.csv')
        # Convert to dictionary format
        circuit_data = df.set_index('Circuit Name').to_dict('index')
        return circuit_data
    except Exception as e:
        print(f"Error loading circuit data: {str(e)}")
        return {}

circuit_data = load_circuit_data()

@app.route('/api/get_circuit_info', methods=['POST'])
def get_circuit_info():
    try:
        # Return all circuit data
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
        weather = data.get('weather', 'clear')  # Default to clear if not specified

        # Get circuit info
        if circuit_name not in circuit_data:
            return jsonify({'error': 'Circuit not found'}), 404
            
        circuit_info = circuit_data[circuit_name]
        track_length = circuit_info['Track Length (km)'] * 1000  # Convert km to meters

        # Load the model
        model = joblib.load('decision_tree_model.pkl')
        
        # Prepare data for prediction
        new_data = pd.DataFrame({
            'tire_wear': [tire_wear],
            'race_position': [race_position],
            'track_length': [track_length]
        })
        
        predicted_time = model.predict(new_data)
        
        # Adjust pit threshold based on weather
        base_threshold = 85
        pit_threshold = base_threshold * 1.2 if weather == 'rain' else base_threshold
        
        pit_decision = "Pit" if predicted_time[0] > pit_threshold else "No Pit"

        return jsonify({
            'predicted_lap_time': float(predicted_time[0]),
            'pit_decision': pit_decision,
            'circuit': circuit_name,
            'track_type': circuit_info['Track Type'],
            'average_wear_rate': circuit_info['Average Wear Rate']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)