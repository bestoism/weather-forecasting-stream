import streamlit as st
import time

# Konfigurasi Halaman
st.set_page_config(
    page_title="Weather Stream Indonesia",
    page_icon="🌦️",
    layout="wide"
)

# Judul Dashboard
st.title("🇮🇩 Real-Time Weather Forecasting Stream")

# Placeholder text
st.write("Selamat datang di dashboard cuaca. Project ini sedang dalam tahap inisialisasi.")

# Sidebar simulasi
st.sidebar.header("Konfigurasi")
provinsi = st.sidebar.selectbox(
    "Pilih Provinsi",
    ["DKI Jakarta", "Jawa Barat", "Jawa Timur", "Bali"] # Nanti kita lengkapi jadi 38
)

st.write(f"Menampilkan data untuk: **{provinsi}**")