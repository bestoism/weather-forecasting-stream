import requests
import pandas as pd
import os
from datetime import datetime
import streamlit as st

# File CSV untuk menyimpan database cuaca sementara
CSV_FILE = "weather_history.csv"

def get_real_weather(lat, lon):
    """
    Mengambil data real-time dari OpenWeatherMap API
    """
    api_key = st.secrets["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            return {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
                "provinsi_lat": lat, # Kita simpan lat/lon sebagai penanda lokasi
                "provinsi_lon": lon
            }
        else:
            st.error(f"Error API: {data.get('message', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Failed to connect: {e}")
        return None

def save_to_csv(data_dict):
    """
    Menyimpan satu baris data ke file CSV.
    Jika file belum ada, buat baru dengan header.
    """
    if data_dict is None:
        return

    df_new = pd.DataFrame([data_dict])
    
    # Cek apakah file sudah ada
    if not os.path.exists(CSV_FILE):
        df_new.to_csv(CSV_FILE, index=False)
    else:
        # Append mode (menambahkan di baris paling bawah)
        df_new.to_csv(CSV_FILE, mode='a', header=False, index=False)

def load_data_from_csv(lat, lon):
    """
    Membaca data dari CSV khusus untuk provinsi yang dipilih (filter by lat/lon)
    """
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame() # Return empty dataframe
    
    df = pd.read_csv(CSV_FILE)
    
    # Filter data hanya untuk koordinat provinsi yang sedang dipilih user
    # Kita pakai toleransi float sedikit agar akurat
    filtered_df = df[
        (df['provinsi_lat'].astype(float).round(4) == round(lat, 4)) & 
        (df['provinsi_lon'].astype(float).round(4) == round(lon, 4))
    ]
    
    return filtered_df