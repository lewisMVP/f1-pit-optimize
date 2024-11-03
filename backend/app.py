from flask import Flask, jsonify, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

app = Flask(__name__)

# Initialize and train the linear regression model
def train_model():
    # Sample data for training the model
    data = {
        'lap_time': [85, 90, 78, 92, 84, 87],  # Lap time (seconds)
        'tire_wear': [0.2, 0.25, 0.15, 0.3, 0.22, 0.18],  # Tire wear (from 0 to 1)
        'race_position': [1, 2, 3, 4, 5, 6]  # Example race positions
    }
    df = pd.DataFrame(data)

    # Split data into independent variables (X) and dependent variable (y)
    X = df[['tire_wear', 'race_position']]  # Independent variables
    y = df['lap_time']  # Dependent variable

    # Initialize the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Save the model
    joblib.dump(model, 'linear_regression_model.pkl')

# Endpoint to get pit stop decision
@app.route('/api/get_pit_decision', methods=['POST'])
def get_pit_decision():
    try:
        data = request.get_json()
        tire_wear = data['tire_health']  # Using tire_health
        race_position = data['race_position']  # Using race position

        # Load the trained model
        model = joblib.load('linear_regression_model.pkl')

        # Predict lap time based on tire wear and race position
        new_data = pd.DataFrame({'tire_wear': [tire_wear], 'race_position': [race_position]})
        predicted_time = model.predict(new_data)

        # Logic to decide pit or no pit
        pit_threshold = 85  # Example threshold for lap time (in seconds)
        pit_decision = "Pit" if predicted_time[0] < pit_threshold else "No Pit"

        return jsonify({'predicted_lap_time': predicted_time[0], 'pit_decision': pit_decision})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    train_model()  # Train the model when the application starts
    app.run(debug=True)
