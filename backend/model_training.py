# model_training.py
import fastf1
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

def get_f1_data():
    # Enable cache
    fastf1.Cache.enable_cache('cache')
    
    race_data = []
    # Get data from 2018-2023 seasons
    for year in range(2018, 2024):
        try:
            for race in fastf1.get_event_schedule(year):
                session = fastf1.get_session(year, race['EventName'], 'R')
                session.load()
                
                # Get car telemetry data
                laps = session.laps
                tel = laps.get_telemetry()
                
                # Extract relevant features
                for index, lap in laps.iterrows():
                    race_data.append({
                        'track_name': race['EventName'],
                        'track_length': race['CircuitLength'],
                        'car_speed': tel['Speed'].mean(),
                        'tyre_life': lap['TyreLife'] if 'TyreLife' in lap else None,
                        'position': lap['Position'],
                        'lap_time': lap['LapTime'].total_seconds() if pd.notna(lap['LapTime']) else None
                    })
        except Exception as e:
            print(f"Error processing {year}: {str(e)}")
            continue
    
    return pd.DataFrame(race_data)

def train_model():
    # Get F1 data
    df = get_f1_data()
    
    # Clean data
    df = df.dropna()
    
    # Prepare features
    X = df[['car_speed', 'tyre_life', 'track_length', 'position']]
    y = df['lap_time']
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Save model
    joblib.dump(model, 'f1_prediction_model.pkl')
    
    return model

if __name__ == '__main__':
    train_model()