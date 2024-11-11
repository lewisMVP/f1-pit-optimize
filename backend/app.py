from flask import Flask, jsonify, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

# Load circuit data from CSV
def load_circuit_data():
    # Read the CSV file containing circuit information
    df = pd.read_csv('circuits.csv')
    # Set 'Circuit Name' as the index to make it easier to look up circuits by name
    circuit_data = df.set_index('Circuit Name').T.to_dict('dict')
    return circuit_data

circuit_data = load_circuit_data()  # Load the data at the start

# Train the model using sample data
def train_model():
    # Sample data for training
    data = {
        'lap_time': [85, 90, 78, 92, 84, 87],  # Lap time in seconds
        'tire_wear': [0.2, 0.25, 0.15, 0.3, 0.22, 0.18],  # Tire wear (from 0 to 1)
        'race_position': [1, 2, 3, 4, 5, 6],  # Example race positions
        'track_length': [5000, 5000, 5000, 5000, 5000, 5000]  # Track length in meters
    }
    df = pd.DataFrame(data)
    
    X = df[['tire_wear', 'race_position', 'track_length']]
    y = df['lap_time']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Save the model to a file
    joblib.dump(model, 'linear_regression_model.pkl')

# Endpoint to retrieve circuit information
@app.route('/api/get_circuit_info', methods=['POST'])
def get_circuit_info():
    try:
        data = request.get_json()
        circuit_name = data.get('circuit_name')
        
        # Fetch the circuit information from the loaded data
        if circuit_name in circuit_data:
            return jsonify(circuit_data[circuit_name])
        else:
            return jsonify({'error': 'Circuit not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to get pit stop decision based on model prediction
@app.route('/api/get_pit_decision', methods=['POST'])
def get_pit_decision():
    try:
        data = request.get_json()
        tire_wear = data['tire_wear']
        race_position = data['race_position']
        circuit_name = data['circuit_name']
        
        # Get track length and average wear rate from the selected circuit
        circuit_info = circuit_data.get(circuit_name)
        if not circuit_info:
            return jsonify({'error': 'Circuit not found'}), 404

        track_length = circuit_info['Track Length (km)'] * 1000  # Convert km to meters

        model = joblib.load('linear_regression_model.pkl')
        new_data = pd.DataFrame({'tire_wear': [tire_wear], 'race_position': [race_position], 'track_length': [track_length]})
        predicted_time = model.predict(new_data)
        
        pit_threshold = 85
        pit_decision = "Pit" if predicted_time[0] < pit_threshold else "No Pit"
        
        return jsonify({
            'predicted_lap_time': predicted_time[0],
            'pit_decision': pit_decision,
            'circuit': circuit_name,
            'track_type': circuit_info['Track Type'],
            'average_wear_rate': circuit_info['Average Wear Rate']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    train_model()  # Train the model on startup
    app.run(debug=True, port=5000)
