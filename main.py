import streamlit as st
import pandas as pd
import time
import plotly.express as px
from const import PROVINCES
from utils import get_real_weather, save_to_csv, load_data_from_csv

st.set_page_config(page_title="Real Weather Stream", page_icon="🌤️", layout="wide")

st.title("🇮🇩 Live Real-World Weather Monitor")

# --- SIDEBAR ---
st.sidebar.header("Lokasi Monitor")
selected_prov = st.sidebar.selectbox("Pilih Provinsi", list(PROVINCES.keys()))
lat = PROVINCES[selected_prov]["lat"]
lon = PROVINCES[selected_prov]["lon"]

st.sidebar.write("---")

# Slider Interval Update
update_interval = st.sidebar.slider("Update Interval (detik)", min_value=10, max_value=600, value=60)
is_running = st.sidebar.checkbox("Start Monitoring", value=False)

# --- MAIN DISPLAY ---
col_kiri, col_kanan = st.columns([2, 1])

with col_kanan:
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=6, use_container_width=True)

with col_kiri:
    # PERBAIKAN DISINI: Gunakan st.empty() agar isinya di-replace, bukan di-append
    metrics_placeholder = st.empty() 
    chart_placeholder = st.empty()

# --- FUNGSI UTAMA ---
def render_ui():
    # 1. Load Data dari CSV Local
    df_history = load_data_from_csv(lat, lon)
    
    if not df_history.empty:
        # Ambil data paling baru
        last_data = df_history.iloc[-1]
        
        # PERBAIKAN: Masukkan layout kolom ke dalam placeholder container
        with metrics_placeholder.container():
            c1, c2, c3 = st.columns(3)
            c1.metric("Suhu", f"{last_data['temperature']} °C")
            c2.metric("Kecepatan Angin", f"{last_data['wind_speed']} km/h")
            c3.metric("Arah Angin", f"{last_data['wind_direction']}°")
            st.caption(f"Last Update: {last_data['timestamp']} (Via Open-Meteo Free)")

        # Tampilkan Grafik History
        with chart_placeholder.container():
            fig = px.line(df_history, x='timestamp', y='temperature', 
                          title=f"History Suhu Real: {selected_prov}", markers=True)
            
            # Atur tinggi grafik dan format
            fig.update_layout(height=350, yaxis_title="Suhu (°C)", xaxis_title="Waktu")
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        # Tampilkan pesan di placeholder jika kosong
        metrics_placeholder.info("Belum ada data history. Klik 'Start Monitoring'.")

# --- LOOPING ---
if is_running:
    countdown_placeholder = st.empty()
    
    while True:
        # 1. Fetch Data Baru
        with st.spinner(f"Mengambil data real-time dari {selected_prov}..."):
            new_data = get_real_weather(lat, lon)
            if new_data:
                save_to_csv(new_data)
        
        # 2. Render Ulang UI
        render_ui()
        
        # 3. Countdown Timer
        for i in range(update_interval, 0, -1):
            countdown_placeholder.text(f"⏳ Mengambil data lagi dalam {i} detik...")
            time.sleep(1)
            
        countdown_placeholder.empty() 

else:
    render_ui()
    st.warning("Monitoring dimatikan. Klik 'Start Monitoring' di sidebar.")