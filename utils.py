import pandas as pd
import random

# --- DATA KLINIK SELANGOR ---
DATA_KLINIK = [
    {"name": "KK Seksyen 7 Shah Alam", "lat": 3.0753, "lon": 101.4877},
    {"name": "KK Bandar Baru Bangi", "lat": 2.9608, "lon": 101.7554},
    {"name": "KK Kajang", "lat": 2.9935, "lon": 101.7874},
    {"name": "KK Klang", "lat": 3.0453, "lon": 101.4430},
    {"name": "KK Puchong", "lat": 3.0336, "lon": 101.6174}
]

# --- FUNGSI GENERATE DATA ---
def generate_doctors(klinik_name):
    random.seed(klinik_name) 
    jumlah = random.randint(10, 15)
    names = ["Dr. Ali", "Dr. Siti", "Dr. Ah Meng", "Dr. Raju", "Dr. Sarah", "Dr. David", "Dr. Mei Ling", "Dr. Farhana"]
    data = []
    for _ in range(jumlah):
        nama = random.choice(names) + f" ({random.randint(100,999)})"
        skor = random.randint(75, 99)
        status = "Cemerlang" if skor > 90 else ("Baik" if skor > 80 else "Sederhana")
        data.append({"Nama Pegawai": nama, "Jabatan": "Pesakit Luar", "Skor Semasa": skor, "Status": status})
    return pd.DataFrame(data)