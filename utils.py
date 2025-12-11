import random

def generate_initial_data():
    """
    Membuat data awal random yang masuk akal untuk Indonesia (Tropis)
    """
    return {
        "temperature": random.uniform(26.0, 33.0), # Celcius
        "humidity": random.uniform(60.0, 90.0),    # Persen
        "wind_speed": random.uniform(5.0, 20.0),   # km/h
        "pressure": random.uniform(1005.0, 1015.0) # hPa
    }

def update_weather_data(current_data):
    """
    Fungsi ini mengambil data terakhir, lalu mengubahnya sedikit (fluktuasi)
    agar terlihat seperti data sensor asli yang bergerak live.
    """
    # Fluktuasi kecil (Random Walk)
    delta_temp = random.uniform(-0.1, 0.1)
    delta_humid = random.uniform(-0.5, 0.5)
    delta_wind = random.uniform(-0.5, 0.5)
    delta_pressure = random.uniform(-0.1, 0.1)

    new_data = {
        "temperature": round(current_data["temperature"] + delta_temp, 2),
        "humidity": round(max(0, min(100, current_data["humidity"] + delta_humid)), 1),
        "wind_speed": round(max(0, current_data["wind_speed"] + delta_wind), 1),
        "pressure": round(current_data["pressure"] + delta_pressure, 1)
    }
    
    return new_data