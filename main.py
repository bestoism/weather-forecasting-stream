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

# Pengaturan Interval Update
# JANGAN terlalu cepat (misal 1 detik) karena API ada limitnya & data cuaca gak berubah secepat itu.
# Rekomendasi: 300 detik (5 menit) atau 600 detik (10 menit).
update_interval = st.sidebar.slider("Update Interval (detik)", min_value=10, max_value=600, value=60)
is_running = st.sidebar.checkbox("Start Monitoring", value=False)

# --- MAIN DISPLAY ---
# Placeholder untuk UI
col_kiri, col_kanan = st.columns([2, 1])

with col_kanan:
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=6, use_container_width=True)

with col_kiri:
    metrics_container = st.container()
    chart_container = st.empty()

# --- FUNGSI UTAMA ---
def render_ui():
    # 1. Load Data dari CSV Local
    df_history = load_data_from_csv(lat, lon)
    
    if not df_history.empty:
        # Ambil data paling baru (baris terakhir)
        last_data = df_history.iloc[-1]
        
        # Tampilkan Metrik
        with metrics_container:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Suhu", f"{last_data['temperature']} °C")
            c2.metric("Kelembaban", f"{last_data['humidity']} %")
            c3.metric("Angin", f"{last_data['wind_speed']} m/s")
            c4.metric("Tekanan", f"{last_data['pressure']} hPa")
            st.caption(f"Last API Fetch: {last_data['timestamp']}")

        # Tampilkan Grafik History
        with chart_container:
            fig = px.line(df_history, x='timestamp', y='temperature', 
                          title=f"History Suhu Real: {selected_prov}", markers=True)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data history untuk provinsi ini. Silakan mulai monitoring.")

# --- LOOPING ---
if is_running:
    # Placeholder kosong untuk countdown
    countdown_placeholder = st.empty()
    
    while True:
        # 1. Fetch Data Baru dari API
        with st.spinner(f"Mengambil data real-time dari {selected_prov}..."):
            new_data = get_real_weather(lat, lon)
            if new_data:
                save_to_csv(new_data) # Simpan ke CSV
        
        # 2. Render Ulang UI (Baca dari CSV yang baru diupdate)
        render_ui()
        
        # 3. Countdown Timer (Supaya user tau kapan update berikutnya)
        for i in range(update_interval, 0, -1):
            countdown_placeholder.text(f"⏳ Mengambil data lagi dalam {i} detik...")
            time.sleep(1)
            
        # Clear ulang untuk loop berikutnya
        countdown_placeholder.empty() 

else:
    # Jika tidak running, tetap tampilkan data terakhir yang ada di CSV (jika ada)
    render_ui()
    st.warning("Monitoring dimatikan. Klik 'Start Monitoring' di sidebar.")