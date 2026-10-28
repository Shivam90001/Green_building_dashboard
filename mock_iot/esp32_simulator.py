import time
import requests
import random
from datetime import datetime

API_INGEST_URL = "http://127.0.0.1:5000/api/iot/ingest"
API_SETTINGS_URL = "http://127.0.0.1:5000/api/settings"

print("==================================================")
print("     ESP32 MICROCONTROLLER RIG SIMULATOR          ")
print("==================================================")
print(f"Target API Server: {API_INGEST_URL}")
print("Sensors Simulated: PZEM-004T, YF-S201, DHT11")
print("Streaming frequency: every 5 seconds")
print("Press Ctrl+C to terminate simulation.")
print("==================================================")

session = requests.Session()

# Keep track of active state
energy_base = 1200
water_base = 6
temp_base = 22
hum_base = 45

while True:
    try:
        # Check active server mode
        try:
            res = session.get(API_SETTINGS_URL, timeout=3)
            if res.status_code == 200:
                settings = res.json()
                if settings.get("mode") != "LIVE":
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Server is currently in DEMO mode. Ingestion paused...")
                    time.sleep(5)
                    continue
        except requests.exceptions.RequestException:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Cannot connect to server API. Is Flask running on port 5000?")
            time.sleep(5)
            continue

        # Simulate PZEM-004T Electrical load
        # 10% chance of a high power usage spike exceeding 3500W threshold
        if random.random() < 0.12:
            energy_val = random.uniform(3600, 4800)
            print("⚡ [SIMULATOR ALERT] Simulating high load spike on PZEM-004T node!")
        else:
            # Diurnal simulation based on actual hour
            hour = datetime.now().hour
            activity_multiplier = 2.2 if (8 <= hour <= 18) else 0.6
            energy_val = energy_base * activity_multiplier + random.uniform(-100, 150)
            energy_val = max(50.0, energy_val)

        # Simulate YF-S201 Water flow rate
        # 10% chance of a flow surge exceeding 25 L/min
        if random.random() < 0.10:
            water_val = random.uniform(26, 35)
            print("💧 [SIMULATOR ALERT] Simulating water surge/leakage on YF-S201 node!")
        else:
            # Flow occurs during usage hours
            water_val = water_base + random.uniform(-2, 4) if (7 <= datetime.now().hour <= 22) else random.uniform(0.1, 1.2)
            water_val = max(0.0, water_val)

        # Simulate DHT11 Climate conditions
        # 8% chance of server room heating spike exceeding 28°C
        if random.random() < 0.08:
            temp_val = random.uniform(29.0, 33.0)
            hum_val = random.uniform(62.0, 75.0)
            print("🌡️ [SIMULATOR ALERT] Simulating server room cooling failure on DHT11 node!")
        else:
            temp_val = temp_base + random.uniform(-1.0, 1.5)
            hum_val = hum_base + random.uniform(-5.0, 6.0)

        # POST PZEM-004T Energy
        payload_energy = {"node_id": "node_energy", "value1": round(energy_val, 2)}
        session.post(API_INGEST_URL, json=payload_energy, timeout=3)

        # POST YF-S201 Water
        payload_water = {"node_id": "node_water", "value1": round(water_val, 2)}
        session.post(API_INGEST_URL, json=payload_water, timeout=3)

        # POST DHT11 Climate
        payload_climate = {"node_id": "node_climate", "value1": round(temp_val, 2), "value2": round(hum_val, 2)}
        session.post(API_INGEST_URL, json=payload_climate, timeout=3)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Streamed metrics -> Energy: {round(energy_val, 1)} W, Water: {round(water_val, 1)} L/m, Temp: {round(temp_val, 1)}°C, Hum: {round(hum_val, 1)}%")

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Ingestion error: {str(e)}")

    time.sleep(5)
