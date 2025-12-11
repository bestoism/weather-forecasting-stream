import requests
import pandas as pd
import os
from datetime import datetime
import streamlit as st

# File CSV penyimpanan
CSV_FILE = "weather_history.csv"

def get_real_weather(lat, lon):
    """
    Mengambil data real-time dari Open-Meteo (Gratis, Tanpa API Key)
    """
    # Kita minta data: Temperature, Wind Speed, Wind Direction
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Cek apakah responnya valid
        if "current_weather" in data:
            current = data["current_weather"]
            return {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "temperature": current["temperature"],
                "wind_speed": current["windspeed"],
                "wind_direction": current["winddirection"],
                # Open-Meteo basic tidak langsung kasih humidity, kita set 0 dulu biar ga error
                "humidity": 0,    
                "pressure": 0,    
                "provinsi_lat": lat,
                "provinsi_lon": lon
            }
        else:
            return None
            
    except Exception as e:
        st.error(f"Koneksi Error: {e}")
        return None

def save_to_csv(data_dict):
    if data_dict is None:
        return

    df_new = pd.DataFrame([data_dict])
    
    if not os.path.exists(CSV_FILE):
        df_new.to_csv(CSV_FILE, index=False)
    else:
        df_new.to_csv(CSV_FILE, mode='a', header=False, index=False)

def load_data_from_csv(lat, lon):
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()
    
    df = pd.read_csv(CSV_FILE)
    
    # Filter data sesuai lokasi
    filtered_df = df[
        (df['provinsi_lat'].astype(float).round(4) == round(lat, 4)) & 
        (df['provinsi_lon'].astype(float).round(4) == round(lon, 4))
    ]
    
    return filtered_df