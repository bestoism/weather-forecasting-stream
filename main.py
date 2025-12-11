import streamlit as st
import pandas as pd
import time
import plotly.express as px # Kita siapkan untuk grafik nanti
from const import PROVINCES
from utils import generate_initial_data, update_weather_data

# Konfigurasi Halaman
st.set_page_config(
    page_title="Weather Stream Indonesia",
    page_icon="🌦️",
    layout="wide"
)

# --- 1. SETUP SESSION STATE ---
# Kita butuh ingatan (memory) untuk menyimpan data sebelumnya agar grafik nyambung
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = generate_initial_data()

# --- 2. SIDEBAR ---
st.sidebar.header("Konfigurasi Lokasi")
nama_provinsi = list(PROVINCES.keys())
selected_prov = st.sidebar.selectbox("Pilih Provinsi", nama_provinsi)

lat = PROVINCES[selected_prov]["lat"]
lon = PROVINCES[selected_prov]["lon"]

st.sidebar.markdown(f"**Lat:** `{lat}` | **Lon:** `{lon}`")
st.sidebar.markdown("---")
# Tombol untuk start/stop stream (opsional, tapi berguna)
run_stream = st.sidebar.checkbox("🔴 LIVE STREAMING", value=True)

# --- 3. MAIN UI LAYOUT ---
st.title("🇮🇩 Real-Time Weather Forecasting Stream")

# Baris 1: Metric Cards (Placeholder)
# Kita siapkan 'wadah' kosong (container) yang nanti akan kita isi ulang terus menerus
metric_placeholder = st.empty()

# Baris 2: Peta (Static, tidak perlu di-looping berat)
col_map = st.container()
with col_map:
    st.subheader(f"Lokasi: {selected_prov}")
    map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_df, zoom=5, use_container_width=True)

# --- 4. STREAMING LOOP ---
if run_stream:
    while True:
        # 1. Update data simulasi
        st.session_state.weather_data = update_weather_data(st.session_state.weather_data)
        current = st.session_state.weather_data
        
        # 2. Tampilkan Data ke dalam Placeholder yang sudah disiapkan di atas
        with metric_placeholder.container():
            # Bagi menjadi 4 kolom metrik
            k1, k2, k3, k4 = st.columns(4)
            
            k1.metric(label="Temperature", value=f"{current['temperature']} °C", delta=f"{current['temperature'] - 28:.1f} vs Avg")
            k2.metric(label="Humidity", value=f"{current['humidity']} %")
            k3.metric(label="Wind Speed", value=f"{current['wind_speed']} km/h")
            k4.metric(label="Pressure", value=f"{current['pressure']} hPa")
            
            # Kita kasih info kecil bahwa ini live
            st.caption(f"Last updated: {time.strftime('%H:%M:%S')}")

        # 3. Jeda waktu (Simulasi 1 detik sekali)
        time.sleep(1) 
        
        # NOTE: Di Streamlit, loop 'while True' akan berjalan terus. 
        # Jika user mengganti dropdown provinsi, Streamlit akan otomatis
        # me-restart script dari atas, sehingga loop baru akan terbentuk dengan provinsi baru.
else:
    st.warning("Stream dimatikan. Centang 'LIVE STREAMING' di sidebar untuk memulai.")