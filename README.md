# 🌲 ForageCast AI

ForageCast AI is a real-time, micro-climate dashboard that uses live satellite weather data and the TabPFN Foundation Model to predict optimal foraging conditions in Punjab, India. 

*Built for the Hacktoberfest 2026 Open-Source AI Challenge ("Touch Grass" theme).* 

## 🏗 Architecture & Tech Stack

This project is built around a lightweight, open-weight architecture that runs zero-shot inference locally on the CPU.

### 1. The Frontend (UI)
- **Streamlit**: A highly reactive Python web framework used to build the dashboard.
- **Custom Styling**: Uses injected inline CSS to bypass standard Streamlit limitations, achieving a beautiful, glassmorphism-inspired dark mode UI with a nature theme.

### 2. The Data Pipeline (Open-Meteo API)
- **Live Satellite Data**: The app fetches real-time micro-climate metrics (Temperature, Humidity, 7-Day Rainfall, and Soil Moisture at 0-7cm) via the free, open-source Open-Meteo API.
- **Synthetic Dataset Generation**: Includes a data generation script (`fetch_real_data.py`) that pulls 365 days of historical weather data and applies botanical logic to label days as optimal or suboptimal for fruiting.

### 3. The AI Brain (TabPFN)
- **Foundation Model**: Uses [TabPFN](https://github.com/automl/TabPFN), a Prior-Data Fitted Network that specializes in tabular data.
- **Zero-Shot Inference**: Instead of traditional gradient descent training, the generated CSV of historical micro-climates is passed directly into TabPFN at runtime. The model instantly generalizes the decision boundaries on the CPU in under a second.

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- A TabPFN Token (for TabPFN 9.1.0+)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/foragecast-ai.git
   cd foragecast-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your TabPFN API key:
   Create a `.env` file in the root directory and add your token:
   ```
   TABPFN_TOKEN=your_token_here
   ```

5. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

## 📜 License
MIT License
