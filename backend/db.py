import sqlite3
import os
import hashlib
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    print(f"Initializing database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_nodes (
        node_id TEXT PRIMARY KEY,
        name TEXT,
        sensor_type TEXT,
        threshold REAL,
        calibration_factor REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id TEXT,
        value1 REAL,
        value2 REAL,
        mode TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        building_id TEXT DEFAULT 'building_a',
        FOREIGN KEY (node_id) REFERENCES sensor_nodes(node_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id TEXT,
        reading_value REAL,
        threshold REAL,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        resolved INTEGER DEFAULT 0,
        building_id TEXT DEFAULT 'building_a',
        FOREIGN KEY (node_id) REFERENCES sensor_nodes(node_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT
    )
    ''')

    # Insert default settings
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('active_mode', 'LIVE')")

    # Insert default sensor nodes
    cursor.execute("INSERT OR IGNORE INTO sensor_nodes VALUES ('node_energy', 'Main Office Energy Node', 'PZEM-004T', 3500.0, 1.0)")
    cursor.execute("INSERT OR IGNORE INTO sensor_nodes VALUES ('node_water', 'Ground Water Supply Line', 'YF-S201', 25.0, 1.0)")
    cursor.execute("INSERT OR IGNORE INTO sensor_nodes VALUES ('node_climate', 'Server Room Climate', 'DHT11', 28.0, 1.0)") # Temp threshold 28 C

    # Insert default admin user (password: admin123)
    admin_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin', ?)", (admin_hash,))

    # Check if there are readings already. If not, populate with historical baseline data
    cursor.execute("SELECT COUNT(*) FROM sensor_readings")
    if cursor.fetchone()[0] == 0:
        print("Populating historical baseline data for multiple buildings (DEMO mode)...")
        now = datetime.now()
        readings_to_insert = []

        buildings = {
            'building_a': { # Office block
                'energy': (800, 2500, 7, 19), # base night, base day, business start, business end
                'water': (2, 14, 8, 18),
                'temp': (21, 24)
            },
            'building_b': { # Research Lab
                'energy': (1800, 4800, 0, 24), # 24/7 server loading
                'water': (1, 6, 9, 17),
                'temp': (18, 20)
            },
            'building_c': { # Academic Block
                'energy': (200, 3200, 8, 17), # shutdown at night
                'water': (1, 28, 8, 17), # high water surge during class breaks
                'temp': (22, 26)
            }
        }

        # Generate 48 hours of historical hourly data for DEMO mode
        for b_id, profile in buildings.items():
            for hour in range(48):
                ts = (now - timedelta(hours=hour)).strftime('%Y-%m-%d %H:%M:%S')
                hour_of_day = (now - timedelta(hours=hour)).hour

                # Energy
                en_night, en_day, start_h, end_h = profile['energy']
                is_active = start_h <= hour_of_day <= end_h if start_h != end_h else True
                energy_val = (en_day if is_active else en_night) + random.uniform(-150, 250)
                readings_to_insert.append(('node_energy', energy_val, None, 'DEMO', ts, b_id))

                # Water
                wat_night, wat_day, start_w, end_w = profile['water']
                is_water_active = start_w <= hour_of_day <= end_w
                water_val = (wat_day if is_water_active else wat_night) + random.uniform(-1, 3)
                water_val = max(0.0, water_val)
                readings_to_insert.append(('node_water', water_val, None, 'DEMO', ts, b_id))

                # Climate (Temperature and Humidity)
                t_min, t_max = profile['temp']
                is_warm = 12 <= hour_of_day <= 16
                temp_val = (t_max if is_warm else t_min) + random.uniform(-0.8, 1.2)
                humidity_val = (45 if is_warm else 55) + random.uniform(-4.0, 5.0)
                readings_to_insert.append(('node_climate', temp_val, humidity_val, 'DEMO', ts, b_id))

        cursor.executemany("""
            INSERT INTO sensor_readings (node_id, value1, value2, mode, timestamp, building_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, readings_to_insert)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
