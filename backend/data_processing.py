import pandas as pd
import numpy as np

# Define the number of rows of data you want to create
num_rows = 100

# Create synthetic data
data = {
    'lap_time': np.random.uniform(70, 120, num_rows),        # Lap times between 70 to 120 seconds
    'tyre_wear': np.random.uniform(0, 1, num_rows),          # Tyre wear between 0 (new) and 1 (worn out)
    'race_position': np.random.randint(1, 21, num_rows),     # Race positions between 1 and 20
    'track_length': np.random.uniform(3000, 7000, num_rows)  # Track length between 3000 meters (3 km) and 7000 meters (7 km)
}

# Create a DataFrame
df_test = pd.DataFrame(data)

# Save to CSV file
df_test.to_csv('f1_test_data.csv', index=False)

print("Test data CSV file created: f1_test_data.csv")
