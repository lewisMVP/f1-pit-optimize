from flask import Flask, jsonify, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from flask_cors import CORS
import fastf1 as ff1
import logging
# Initialize and train the linear regression model
import joblib
import os
app = Flask(__name__)
CORS(app)

# Load the f1dataR library
years = range(2018, 2024)
all_events = []

for year in years:
    try:
        # List the rounds for the specific season/year
        for round_number in range(1, 23):  # Update the range according to the number of races in each season
            session = ff1.get_session(year, round_number, 'R')  # 'R' stands for Race session
            session.load()  # Load the session data
            events = session.get_events()  # Get the events for the session
            all_events.extend(events)  # Append the events to the all_events list
    except Exception as e:
        print(f"Error loading session for year {year}, round {round_number}: {e}")

def train_model():
    try:
        # Tải dữ liệu đào tạo
        data = pd.read_csv(data_path)

        # Định nghĩa biến model
        X = data[['tire_wear', 'race_position', 'track_length']]  # Independent variables
        y = data['lap_time']  # Dependent variable

        model = LinearRegression()
        model.fit(X, y)

        # Lưu trữ mô hình đã đào tạo vào tệp tin.pkl
        joblib.dump(model, linear_regression_model_path)

    except Exception as e:
        print(f"Error training model: {e}")

# Load the trained model
model = joblib.load('linear_regression_model.pkl')

# Endpoint to get event schedule
@app.route('/api/events', methods=['GET'])
def get_events():
    event_data = []
    for event in all_events:
        event_data.append({
            'name': event.name,
            'country': event.country,
            'location': event.location,
            'date': event.date.strftime('%Y-%m-%d'),
            'time': event.time.strftime('%H:%M:%S')
        })
    return jsonify(event_data)

# Endpoint to get pit stop decision
@app.route('/api/get_pit_decision', methods=['POST'])
def get_pit_decision():
    try:
        data = request.get_json()
        tire_wear = data['tire_wear']
        race_position = data['race_position']
        track_length = data['track_length']
        current_lap = data['current_lap']

        new_data = [[tire_wear, race_position, track_length]]
        predicted_time = model.predict(new_data)[0]

        PIT_THRESHOLD = 72.12  # Adjust this threshold as needed
        pit_decision = "Pit" if predicted_time > PIT_THRESHOLD else "No Pit"

        return jsonify({
            'predicted_lap_time': predicted_time,
            'pit_decision': pit_decision,
            'current_lap': current_lap,
            'f1dataR_data': data
        })
    except Exception as e:
        logging.error(f"Error in get_pit_decision: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    train_model()  # Train the model when the application starts
    app.run(debug=True)
    