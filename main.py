import streamlit as st
import pandas as pd
import time
import plotly.express as px 
import plotly.graph_objects as go # Kita pakai graph_objects agar lebih fleksibel kustomisasinya
from const import PROVINCES
from utils import generate_initial_data, update_weather_data

# Konfigurasi Halaman
st.set_page_config(
    page_title="Weather Stream Indonesia",
    page_icon="🌦️",
    layout="wide"
)

# --- SETUP SESSION STATE & HISTORY ---
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = generate_initial_data()

# ### PERUBAHAN STEP 4: Menyiapkan History Data ###
if 'history_temp' not in st.session_state:
    st.session_state.history_temp = []
if 'history_time' not in st.session_state:
    st.session_state.history_time = []

# Batasi history agar tidak memori penuh (misal simpan 50 data terakhir saja)
MAX_HISTORY = 50

# --- SIDEBAR ---
st.sidebar.header("Konfigurasi Lokasi")
nama_provinsi = list(PROVINCES.keys())
selected_prov = st.sidebar.selectbox("Pilih Provinsi", nama_provinsi)

lat = PROVINCES[selected_prov]["lat"]
lon = PROVINCES[selected_prov]["lon"]
st.sidebar.markdown(f"**Lat:** `{lat}` | **Lon:** `{lon}`")
st.sidebar.markdown("---")
run_stream = st.sidebar.checkbox("🔴 LIVE STREAMING", value=True)

# --- MAIN UI ---
st.title("🇮🇩 Real-Time Weather Forecasting Stream")

# Placeholder Containers
metric_placeholder = st.empty()
chart_placeholder = st.empty() # Wadah baru untuk grafik

# Peta (Static)
with st.expander("🗺️ Lihat Peta Lokasi", expanded=False): # Kita lipat biar hemat tempat
    map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_df, zoom=5)

# --- STREAMING LOOP ---
if run_stream:
    while True:
        # 1. Update Data
        st.session_state.weather_data = update_weather_data(st.session_state.weather_data)
        current = st.session_state.weather_data
        
        # 2. Update History (Append Data Baru)
        current_time = time.strftime('%H:%M:%S')
        st.session_state.history_temp.append(current['temperature'])
        st.session_state.history_time.append(current_time)
        
        # Jaga agar list tidak terlalu panjang (FIFO - First In First Out)
        if len(st.session_state.history_temp) > MAX_HISTORY:
            st.session_state.history_temp.pop(0)
            st.session_state.history_time.pop(0)

        # 3. Render Metrik (Angka)
        with metric_placeholder.container():
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Temperature", f"{current['temperature']} °C")
            k2.metric("Humidity", f"{current['humidity']} %")
            k3.metric("Wind Speed", f"{current['wind_speed']} km/h")
            k4.metric("Pressure", f"{current['pressure']} hPa")

        # 4. Render Grafik (Chart)
        with chart_placeholder.container():
            # Kita buat DataFrame sementara dari history
            df_chart = pd.DataFrame({
                "Waktu": st.session_state.history_time,
                "Temperature (°C)": st.session_state.history_temp
            })

            # Buat Line Chart menggunakan Plotly
            fig = px.line(
                df_chart, 
                x="Waktu", 
                y="Temperature (°C)", 
                title=f"Trend Suhu Real-time: {selected_prov}",
                markers=True
            )
            
            # Mempercantik tampilan grafik
            fig.update_layout(
                xaxis_title="Waktu",
                yaxis_title="Suhu (°C)",
                yaxis_range=[20, 40], # Kunci range Y agar grafik tidak lompat-lompat skalanya
                height=400,
                template="plotly_dark" # Tema gelap biar keren
            )
            
            st.plotly_chart(fig, use_container_width=True)

        # 5. Jeda Loop
        time.sleep(1) # Delay 1 detik

else:
    st.warning("Stream dimatikan.")