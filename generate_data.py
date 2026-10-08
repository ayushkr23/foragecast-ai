import pandas as pd
import numpy as np
import os

# Set a seed for reproducibility
np.random.seed(42)

def generate_dataset(filename="foraging_data.csv", n_samples=500):
    print(f"Generating synthetic micro-climate data ({n_samples} samples)...")
    
    # Generate random historical weather/soil data
    data = {
        'temperature_c': np.random.uniform(5, 30, n_samples),
        'humidity_percent': np.random.uniform(30, 95, n_samples),
        'rainfall_mm_last_week': np.random.uniform(0, 80, n_samples),
        'soil_moisture': np.random.uniform(1, 10, n_samples)
    }

    df = pd.DataFrame(data)

    # Define the "ground truth" rules for optimal foraging
    # Example: Wild mushrooms thrive in warm, humid, wet soil.
    # We add randomness so the ML model has to learn probabilities, not just hard rules.
    def is_optimal(row):
        if (15 <= row['temperature_c'] <= 25) and \
           (row['humidity_percent'] > 70) and \
           (row['rainfall_mm_last_week'] > 15) and \
           (row['soil_moisture'] > 6):
            # 90% chance of success in ideal conditions
            return np.random.choice([1, 0], p=[0.9, 0.1])
        else:
            # 5% chance of finding something in poor conditions
            return np.random.choice([1, 0], p=[0.05, 0.95])

    df['optimal_foraging'] = df.apply(is_optimal, axis=1)

    df.to_csv(filename, index=False)
    print(f"Success! Data saved to {filename}")

if __name__ == "__main__":
    generate_dataset()
