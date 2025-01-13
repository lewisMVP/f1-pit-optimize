import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Assuming you have a function to fetch and preprocess data
# from train_model import fetch_and_preprocess_data

# data = fetch_and_preprocess_data(start_year, end_year)
# For example (replace with your actual data fetching):
data = pd.DataFrame({
'lap_time': [85, 90, 78, 92, 84, 87],  # Lap time (seconds)
        'tire_wear': [0.2, 0.25, 0.15, 0.3, 0.22, 0.18],  # Tire wear (from 0 to 1)
        'race_position': [1, 2, 3, 4, 5, 6],  # Example race positions
        'track_length': [5000, 5000, 5000, 5000, 5000, 5000]  # Length of the track in meters
})

X = data[['tire_wear', 'race_position', 'track_length']]
y = data['LapTime']

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, 'linear_regression_model.pkl')
print("Model trained and saved.")