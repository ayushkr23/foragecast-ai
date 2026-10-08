import os
# Load token from .env file before importing TabPFN
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.startswith("TABPFN_TOKEN="):
                os.environ["TABPFN_TOKEN"] = line.strip().split("=")[1].strip('"\'')

import streamlit as st
import pandas as pd
from tabpfn import TabPFNClassifier
import requests
import time

st.set_page_config(page_title="ForageCast AI", page_icon="🌲", layout="wide")

# --- CUSTOM CSS & ANIMATIONS ---
st.markdown("""
<style>
    /* Nature-themed Gradient Button */
    .stButton>button {
        background: linear-gradient(90deg, #2E7D32 0%, #4CAF50 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1.2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        width: 100%;
        margin-top: 20px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.6);
        color: white;
    }
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: rgba(76, 175, 80, 0.05);
        border: 1px solid rgba(76, 175, 80, 0.2);
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    /* Gradient Title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #81C784, #2E7D32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 40px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p style="font-size: 4.5rem; font-weight: 900; background: -webkit-linear-gradient(45deg, #81C784, #2E7D32); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; line-height: 1.2;">🌲 ForageCast AI</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.2rem; color: #888; margin-bottom: 40px;">Powered by TabPFN Foundation Model & Real Climate Data</p>', unsafe_allow_html=True)

# Default coords (Punjab, India)
LAT, LON = 31.1471, 75.3412

@st.cache_data
def load_data():
    if not os.path.exists("real_foraging_data.csv"):
        return None
    return pd.read_csv("real_foraging_data.csv")

if "TABPFN_TOKEN" not in os.environ:
    st.error("⚠️ **TabPFN License Required**")
    st.markdown("""
    **Please follow these steps to authenticate:**
    1. Create a file named `.env` in this project folder.
    2. Add this single line: `TABPFN_TOKEN=your_api_key_here`
    """)
    st.stop()

df = load_data()
if df is None:
    st.error("Real historical data not found. Please run `python fetch_real_data.py` first.")
    st.stop()

features = ['temperature_c', 'humidity_percent', 'rainfall_mm_last_week', 'soil_moisture']
X = df[features]
y = df['optimal_foraging']

@st.cache_resource
def train_model(X_train, y_train):
    clf = TabPFNClassifier(device='cpu')
    clf.fit(X_train, y_train)
    return clf

model = train_model(X, y)

def get_live_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m&daily=precipitation_sum,soil_moisture_0_to_7cm_mean&past_days=7&timezone=auto"
    res = requests.get(url).json()
    
    past_rain = sum(res['daily']['precipitation_sum'][:-1])
    current_temp = res['current']['temperature_2m']
    current_hum = res['current']['relative_humidity_2m']
    current_soil = res['daily']['soil_moisture_0_to_7cm_mean'][-1]
    if current_soil is None:
        current_soil = 0.3
    
    return current_temp, current_hum, past_rain, current_soil

# --- MAIN LAYOUT ---
# Using columns for a modern dashboard look
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.subheader("🌍 Today's Micro-Climate")
    use_live = st.toggle("📡 Sync with Open-Meteo Satellite (Punjab)", value=True)
    
    if use_live:
        try:
            with st.spinner("Triangulating weather data..."):
                temp, humidity, rain, soil = get_live_weather()
                time.sleep(0.5) # Slight delay for cool animation effect
            
            # Dashboard Metrics Layout
            m1, m2 = st.columns(2)
            m3, m4 = st.columns(2)
            m1.metric("Temperature", f"{temp}°C", "Live")
            m2.metric("Humidity", f"{humidity}%", "Live")
            m3.metric("7-Day Rain", f"{rain:.1f} mm", "Accumulated")
            m4.metric("Soil Moisture", f"{soil:.2f} m³/m³", "Live")
            
        except Exception as e:
            st.error("Could not fetch live weather. Check internet.")
            use_live = False

    if not use_live:
        st.info("🔌 Offline Mode Active: Enter local readings manually.")
        temp = st.slider("🌡️ Temperature (°C)", 0.0, 45.0, 25.0)
        humidity = st.slider("💧 Humidity (%)", 10.0, 100.0, 60.0)
        rain = st.slider("🌧️ Rainfall last 7 days (mm)", 0.0, 150.0, 20.0)
        soil = st.slider("🌱 Soil Moisture (m³/m³)", 0.0, 0.6, 0.25)

with col_right:
    st.subheader("🧠 AI Prediction")
    st.write("Feed the data into the TabPFN Foundation Model to see if you should head outside.")
    
    result_container = st.container()
    
    if st.button("🚀 PREDICT FORAGING SUCCESS"):
        with result_container:
            with st.spinner("TabPFN is analyzing historical patterns..."):
                input_data = pd.DataFrame({
                    'temperature_c': [temp],
                    'humidity_percent': [humidity],
                    'rainfall_mm_last_week': [rain],
                    'soil_moisture': [soil]
                })
                
                prediction = model.predict(input_data)[0]
                probability = model.predict_proba(input_data)[0][1] * 100
                
            if prediction == 1:
                st.snow() # Falling nature animation!
                st.success(f"### 🌿 Optimal Conditions!\n**AI Confidence: {probability:.1f}%**")
                st.write("The AI detected patterns matching historical fruiting events. Grab your basket, it's time to touch grass!")
            else:
                st.warning(f"### 🍂 Not Optimal.\n**Chance of success: {probability:.1f}%**")
                st.write("The current conditions don't match the historical growth patterns in Punjab. Wait for a shift in weather.")

st.divider()
st.subheader("📊 The Training Brain")
with st.expander("Click to view the raw 365-day climate history TabPFN learned from"):
    st.dataframe(df, use_container_width=True)
