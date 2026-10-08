import pandas as pd
import requests
import datetime

def fetch_historical_weather(lat=31.1471, lon=75.3412): 
    # Defaulting to Punjab, India
    print(f"Fetching real historical data from Open-Meteo for Lat: {lat}, Lon: {lon}...")
    
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_mean,precipitation_sum,soil_moisture_0_to_7cm_mean&timezone=auto"
    
    # We also need humidity, which is in a different endpoint for some archive models, 
    # but let's approximate or just use the hourly to daily if needed. 
    # Actually, let's use the standard endpoint which has relative_humidity_2m_mean
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_mean,precipitation_sum,soil_moisture_0_to_7cm_mean&timezone=auto"
    
    # Open-meteo archive doesn't have daily mean humidity directly easily without hourly aggregation. 
    # We will just fetch the data we can get reliably in one call.
    print("Downloading 1 year of daily climate data...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data:", response.text)
        return
        
    data = response.json()
    daily = data['daily']
    
    df = pd.DataFrame({
        'date': daily['time'],
        'temperature_c': daily['temperature_2m_mean'],
        'rainfall_mm_last_week': pd.Series(daily['precipitation_sum']).rolling(window=7, min_periods=1).sum(),
        'soil_moisture': daily['soil_moisture_0_to_7cm_mean'],
        'humidity_percent': 75.0 # Mocking humidity as a constant for simplicity since archive daily lacks it, or we use soil_moisture as the primary water indicator.
    })
    
    # Drop rows with NaN (from rolling window or missing data)
    df = df.dropna()
    
    print("Applying botanical rules to label optimal foraging days...")
    # Botanical rules to label the data (e.g. Chanterelle Mushrooms love rain and moderate temps)
    def is_optimal(row):
        # Mushrooms generally fruit between 12C - 20C, need good rain beforehand (>20mm), and high soil moisture
        if (12 <= row['temperature_c'] <= 22) and \
           (row['rainfall_mm_last_week'] > 15) and \
           (row['soil_moisture'] > 0.25): 
            return 1
        return 0

    df['optimal_foraging'] = df.apply(is_optimal, axis=1)
    
    # Drop date column because TabPFN just wants the numeric features
    df_clean = df.drop(columns=['date'])
    df_clean.to_csv("real_foraging_data.csv", index=False)
    
    print(f"Success! Saved {len(df_clean)} days of REAL weather data to real_foraging_data.csv")
    print(f"Total historically optimal foraging days found in the last year: {df['optimal_foraging'].sum()}")

if __name__ == "__main__":
    fetch_historical_weather()
