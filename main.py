import streamlit as st
import pandas as pd
from const import PROVINCES # Import data yang baru dibuat

# Konfigurasi Halaman
st.set_page_config(
    page_title="Weather Stream Indonesia",
    page_icon="🌦️",
    layout="wide"
)

# Judul Dashboard
st.title("🇮🇩 Real-Time Weather Forecasting Stream")

# --- SIDEBAR ---
st.sidebar.header("Konfigurasi Lokasi")

# Dropdown list provinsi dari data const.py
nama_provinsi = list(PROVINCES.keys())
selected_prov = st.sidebar.selectbox("Pilih Provinsi", nama_provinsi)

# Ambil lat/lon berdasarkan pilihan
lat = PROVINCES[selected_prov]["lat"]
lon = PROVINCES[selected_prov]["lon"]

st.sidebar.markdown(f"""
**Koordinat Terpilih:**
- Lintang (Lat): `{lat}`
- Bujur (Lon): `{lon}`
""")

# --- MAIN CONTENT ---
# Buat kolom layout (Kiri: Info, Kanan: Peta)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"Cuaca di {selected_prov}")
    st.info("Sistem siap menerima data stream...")
    # Nanti kita taruh metrik cuaca disini

with col2:
    st.subheader("Peta Lokasi")
    # Siapkan data untuk peta
    map_data = pd.DataFrame({
        'lat': [lat],
        'lon': [lon]
    })
    # Tampilkan peta dengan zoom level tertentu
    st.map(map_data, zoom=6)