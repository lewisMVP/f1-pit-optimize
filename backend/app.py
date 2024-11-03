from flask import Flask, jsonify, request
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

app = Flask(__name__)

# Function to get race track information
def get_race_track_info(track_name):
    url = f"http://api.raceinfo.com/track/{track_name}"
    response = requests.get(url)
    return response.json()

# Function to get weather information
def get_weather_info(location):
    api_key = 'YOUR_API_KEY'  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# Initialize and train the linear regression model
def train_model():
    # Assume you have a DataFrame containing your data
    data = {
        'lap_time': [85, 90, 78, 92, 84, 87],  # Lap time (seconds)
        'tire_wear': [0.2, 0.25, 0.15, 0.3, 0.22, 0.18],  # Tire wear (from 0 to 1)
        'speed': [210, 205, 215, 200, 208, 212]  # Average speed (km/h)
    }
    df = pd.DataFrame(data)

    # Split data into independent variables (X) and dependent variable (y)
    X = df[['tire_wear', 'speed']]  # Independent variables
    y = df['lap_time']  # Dependent variable

    # Initialize the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Save the model
    joblib.dump(model, 'linear_regression_model.pkl')

# Endpoint to get weather information
@app.route('/api/weather')
def weather():
    location = request.args.get('location')
    weather_data = get_weather_info(location)
    return jsonify(weather_data)

# Endpoint to get pit stop decision
@app.route('/api/get_pit_decision', methods=['POST'])
def get_pit_decision():
    try:
        data = request.get_json()
        tire_wear = data['tire_wear']
        speed = data['speed']

        # Load the trained model
        model = joblib.load('linear_regression_model.pkl')

        # Predict pit stop time
        new_data = pd.DataFrame({'tire_wear': [tire_wear], 'speed': [speed]})
        predicted_time = model.predict(new_data)

        # Logic to decide pit or no pit
        pit_threshold = 85  # Example threshold for lap time (in seconds)
        pit_decision = "Pit" if predicted_time[0] < pit_threshold else "No Pit"

        # Print the predicted information
        print(f'Tire wear: {tire_wear}, Speed: {speed} km/h, Predicted lap time: {predicted_time[0]:.2f} seconds, Decision: {pit_decision}')
        
        return jsonify({'predicted_lap_time': predicted_time[0], 'pit_decision': pit_decision})
    except Exception as e:
        print(f"Error: {str(e)}")  # Print error message to console
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    train_model()  # Train the model when the application starts
    app.run(debug=True)
