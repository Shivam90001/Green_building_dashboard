from flask import Flask, request, jsonify, send_from_directory, session
import sqlite3
import os
import hashlib
from datetime import datetime, timedelta
import random
from db import init_db

app = Flask(__name__)
app.secret_key = 'green_building_secret_key_123987' # Hardcoded secret for local dev session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Helper to calculate Building Efficiency Score components
def calculate_scores(energy_val, water_val, temp_val, hum_val, energy_thresh, water_thresh, temp_thresh):
    # 1. Energy Score (ES)
    # Threshold represents target baseline. 0 W = 100 score, threshold W = 70 score, higher drops rapidly.
    if energy_val is None:
        energy_score = 100
    else:
        energy_pct = energy_val / max(1.0, energy_thresh)
        if energy_pct <= 1.0:
            energy_score = 100.0 - (energy_pct * 30.0) # 100 -> 70
        else:
            energy_score = max(0.0, 70.0 - (energy_pct - 1.0) * 100.0)

    # 2. Water Score (WS)
    if water_val is None:
        water_score = 100
    else:
        water_pct = water_val / max(1.0, water_thresh)
        if water_pct <= 1.0:
            water_score = 100.0 - (water_pct * 30.0) # 100 -> 70
        else:
            water_score = max(0.0, 70.0 - (water_pct - 1.0) * 100.0)

    # 3. Climate Score (CS) - ASHRAE 55 Comfort Envelope (20-25°C, 30-60% Humidity)
    if temp_val is None or hum_val is None:
        climate_score = 100
    else:
        temp_penalty = 0
        if temp_val < 20:
            temp_penalty = (20 - temp_val) * 8.0
        elif temp_val > 25:
            temp_penalty = (temp_val - 25) * 8.0

        hum_penalty = 0
        if hum_val < 30:
            hum_penalty = (30 - hum_val) * 1.2
        elif hum_val > 60:
            hum_penalty = (hum_val - 60) * 1.2

        climate_score = max(0.0, 100.0 - temp_penalty - hum_penalty)

    # 4. Weighted Building Efficiency Score
    # Energy: 50%, Water: 30%, Climate: 20%
    weighted_score = (0.50 * energy_score) + (0.30 * water_score) + (0.20 * climate_score)

    return {
        "energy_score": round(energy_score, 1),
        "water_score": round(water_score, 1),
        "climate_score": round(climate_score, 1),
        "building_score": round(weighted_score, 1)
    }

# Check and create threshold alerts
def check_thresholds(conn, node_id, val1, val2=None):
    cursor = conn.cursor()
    cursor.execute("SELECT name, sensor_type, threshold FROM sensor_nodes WHERE node_id = ?", (node_id,))
    node = cursor.fetchone()
    if not node:
        return

    node_name, sensor_type, threshold = node['name'], node['sensor_type'], node['threshold']

    triggered = False
    message = ""

    if node_id == 'node_energy' and val1 > threshold:
        triggered = True
        message = f"Energy consumption spike: {round(val1, 1)} W exceeded threshold of {threshold} W on {node_name}."
    elif node_id == 'node_water' and val1 > threshold:
        triggered = True
        message = f"Water flow rate spike: {round(val1, 1)} L/min exceeded threshold of {threshold} L/min on {node_name}."
    elif node_id == 'node_climate' and val1 > threshold:
        triggered = True
        message = f"Temperature alert: {round(val1, 1)}°C exceeded threshold of {threshold}°C in Server Room."

    if triggered:
        # Check if there is already an unresolved alert of the same type in the last 5 minutes to avoid flooding
        five_mins_ago = (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            SELECT id FROM alerts
            WHERE node_id = ? AND resolved = 0 AND timestamp > ?
        """, (node_id, five_mins_ago))

        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO alerts (node_id, reading_value, threshold, message)
                VALUES (?, ?, ?, ?)
            """, (node_id, val1, threshold, message))
            conn.commit()

# Serve static frontend
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

# --- API ROUTES ---

# Authentication
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        if row['password_hash'] == pwd_hash:
            session['username'] = username
            return jsonify({"success": True, "message": "Login successful"})

    return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"success": True, "message": "Logged out"})

@app.route('/api/auth/session', methods=['GET'])
def get_session():
    if 'username' in session:
        return jsonify({"logged_in": True, "username": session['username']})
    return jsonify({"logged_in": False})

@app.route('/api/iot/ingest', methods=['POST'])
def ingest_iot():
    return jsonify({
        "success": False,
        "message": "Live IoT ingestion is disabled. Use Demo CSV mode."
    }), 403

# CSV Data Upload (Demo / Legacy Mode)
@app.route('/api/demo/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400

    try:
        content = file.read().decode('utf-8')
        lines = content.strip().split('\n')

        # Expect CSV headers: node_id, value1, value2, timestamp
        # Example: node_energy,2400,,2026-08-01 12:00:00
        conn = get_db_connection()
        cursor = conn.cursor()

        # Set mode to DEMO automatically
        cursor.execute("UPDATE settings SET value = 'DEMO' WHERE key = 'active_mode'")

        imported_count = 0
        for line in lines[1:]: # skip header
            parts = line.split(',')
            if len(parts) >= 2:
                node_id = parts[0].strip()
                val1 = float(parts[1].strip())
                val2 = float(parts[2].strip()) if len(parts) > 2 and parts[2].strip() else None
                ts = parts[3].strip() if len(parts) > 3 and parts[3].strip() else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Check node exists
                cursor.execute("SELECT 1 FROM sensor_nodes WHERE node_id = ?", (node_id,))
                if cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO sensor_readings (node_id, value1, value2, mode, timestamp)
                        VALUES (?, ?, ?, 'DEMO', ?)
                    """, (node_id, val1, val2, ts))
                    imported_count += 1

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"Successfully imported {imported_count} historical records. Open the dashboard to visualize them."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error parsing CSV: {str(e)}"}), 500

# Dashboard Statistics & Scores
@app.route('/api/dashboard/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get active mode
    cursor.execute("SELECT value FROM settings WHERE key = 'active_mode'")
    mode = cursor.fetchone()['value']

    # Get current thresholds
    cursor.execute("SELECT node_id, threshold FROM sensor_nodes")
    thresholds = {row['node_id']: row['threshold'] for row in cursor.fetchall()}

    # Get latest readings for each sensor in the current mode
    latest_data = {}
    for node in ['node_energy', 'node_water', 'node_climate']:
        cursor.execute("""
            SELECT value1, value2, timestamp FROM sensor_readings
            WHERE node_id = ? AND mode = ?
            ORDER BY timestamp DESC LIMIT 1
        """, (node, mode))
        row = cursor.fetchone()
        if row:
            latest_data[node] = {
                "val1": row['value1'],
                "val2": row['value2'],
                "timestamp": row['timestamp']
            }
        else:
            latest_data[node] = {"val1": None, "val2": None, "timestamp": None}

    # Fallback to general defaults if no readings exist
    energy_val = latest_data['node_energy']['val1'] or 0.0
    water_val = latest_data['node_water']['val1'] or 0.0
    temp_val = latest_data['node_climate']['val1'] or 23.0
    hum_val = latest_data['node_climate']['val2'] or 45.0

    scores = calculate_scores(
        energy_val, water_val, temp_val, hum_val,
        thresholds.get('node_energy', 3500.0),
        thresholds.get('node_water', 25.0),
        thresholds.get('node_climate', 28.0)
    )

    # Calculate carbon footprint savings
    # Baseline equivalent building carbon footprint vs. current optimized footprint.
    # Energy savings carbon offset: 1 kWh ~ 0.85 kg CO2.
    # Assume target baseline usage is thresholds. Let's calculate actual vs. baseline.
    energy_savings_w = max(0.0, thresholds.get('node_energy', 3500.0) - energy_val)
    carbon_saved_kg = round((energy_savings_w / 1000.0) * 0.85, 2)

    # Get alert counts
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE resolved = 0")
    unresolved_alerts = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "mode": mode,
        "latest_readings": {
            "energy": {
                "val": round(energy_val, 1),
                "unit": "W",
                "timestamp": latest_data['node_energy']['timestamp']
            },
            "water": {
                "val": round(water_val, 1),
                "unit": "L/min",
                "timestamp": latest_data['node_water']['timestamp']
            },
            "climate": {
                "temp": round(temp_val, 1),
                "humidity": round(hum_val, 1),
                "timestamp": latest_data['node_climate']['timestamp']
            }
        },
        "scores": scores,
        "carbon_saved_kg": carbon_saved_kg,
        "unresolved_alerts": unresolved_alerts
    })

# Fetch Chart Data
@app.route('/api/dashboard/charts', methods=['GET'])
def get_charts():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get active mode
    cursor.execute("SELECT value FROM settings WHERE key = 'active_mode'")
    mode = cursor.fetchone()['value']

    # Fetch last 20 readings for charts grouped by time
    chart_data = {
        "labels": [],
        "energy": [],
        "water": [],
        "temp": [],
        "humidity": []
    }

    # Fetch readings for each node in chronologically ascending order (past to present)
    cursor.execute("""
        SELECT timestamp, value1 FROM sensor_readings
        WHERE node_id = 'node_energy' AND mode = ?
        ORDER BY timestamp DESC LIMIT 20
    """, (mode,))
    energy_rows = cursor.fetchall()[::-1] # reverse to get chronological

    cursor.execute("""
        SELECT timestamp, value1 FROM sensor_readings
        WHERE node_id = 'node_water' AND mode = ?
        ORDER BY timestamp DESC LIMIT 20
    """, (mode,))
    water_rows = cursor.fetchall()[::-1]

    cursor.execute("""
        SELECT timestamp, value1, value2 FROM sensor_readings
        WHERE node_id = 'node_climate' AND mode = ?
        ORDER BY timestamp DESC LIMIT 20
    """, (mode,))
    climate_rows = cursor.fetchall()[::-1]

    # Align timestamps. We will use the climate timestamps as the baseline reference,
    # or energy, and align other readings. Or simpler: just zip them.
    # To make it super robust, we extract all unique timestamps and create a timeline.
    timeline = sorted(list(set(
        [r['timestamp'] for r in energy_rows] +
        [r['timestamp'] for r in water_rows] +
        [r['timestamp'] for r in climate_rows]
    )))

    # Keep only the last 20 timestamps
    timeline = timeline[-20:]

    # Create lookups
    energy_map = {r['timestamp']: r['value1'] for r in energy_rows}
    water_map = {r['timestamp']: r['value1'] for r in water_rows}
    temp_map = {r['timestamp']: r['value1'] for r in climate_rows}
    hum_map = {r['timestamp']: r['value2'] for r in climate_rows}

    # Format labels (extract HH:MM:SS)
    for ts in timeline:
        try:
            dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
            label = dt.strftime('%H:%M:%S')
        except:
            label = ts

        chart_data['labels'].append(label)
        chart_data['energy'].append(round(energy_map.get(ts, 0.0), 1))
        chart_data['water'].append(round(water_map.get(ts, 0.0), 1))
        chart_data['temp'].append(round(temp_map.get(ts, 23.0), 1))
        chart_data['humidity'].append(round(hum_map.get(ts, 45.0), 1))

    conn.close()
    return jsonify(chart_data)

# Alerts Management
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 30")
    rows = cursor.fetchall()
    conn.close()

    alerts = []
    for r in rows:
        alerts.append({
            "id": r['id'],
            "node_id": r['node_id'],
            "reading_value": r['reading_value'],
            "threshold": r['threshold'],
            "message": r['message'],
            "timestamp": r['timestamp'],
            "resolved": bool(r['resolved'])
        })
    return jsonify(alerts)

@app.route('/api/alerts/resolve', methods=['POST'])
def resolve_alert():
    data = request.json or {}
    alert_id = data.get('id')
    if not alert_id:
        return jsonify({"success": False, "message": "Missing alert id"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE alerts SET resolved = 1 WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Alert resolved successfully"})

# Settings Page (Get & Update Settings)
@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get active mode
        cursor.execute("SELECT value FROM settings WHERE key = 'active_mode'")
        mode = cursor.fetchone()['value']

        # Get sensor configurations
        cursor.execute("SELECT * FROM sensor_nodes")
        nodes_rows = cursor.fetchall()

        nodes = []
        for r in nodes_rows:
            nodes.append({
                "node_id": r['node_id'],
                "name": r['name'],
                "sensor_type": r['sensor_type'],
                "threshold": r['threshold'],
                "calibration_factor": r['calibration_factor']
            })

        conn.close()
        return jsonify({
            "mode": mode,
            "sensors": nodes
        })

    else: # POST
        # Check authentication in session
        if 'username' not in session:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        data = request.json or {}
        sensors = data.get('sensors') # Array of sensor config objects

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE settings SET value = 'DEMO' WHERE key = 'active_mode'")

        if sensors:
            for s in sensors:
                node_id = s.get('node_id')
                name = s.get('name')
                threshold = s.get('threshold')
                calibration_factor = s.get('calibration_factor')

                if node_id:
                    cursor.execute("""
                        UPDATE sensor_nodes
                        SET name = COALESCE(?, name),
                            threshold = COALESCE(?, threshold),
                            calibration_factor = COALESCE(?, calibration_factor)
                        WHERE node_id = ?
                    """, (name, threshold, calibration_factor, node_id))

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Settings updated successfully"})

# Fetch Raw Data Logs Explorer
@app.route('/api/readings', methods=['GET'])
def get_readings():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get active mode
    cursor.execute("SELECT value FROM settings WHERE key = 'active_mode'")
    mode = cursor.fetchone()['value']

    cursor.execute("""
        SELECT id, node_id, value1, value2, mode, timestamp FROM sensor_readings
        WHERE mode = ?
        ORDER BY timestamp DESC LIMIT 100
    """, (mode,))
    rows = cursor.fetchall()
    conn.close()

    readings = []
    for r in rows:
        readings.append({
            "id": r['id'],
            "node_id": r['node_id'],
            "value1": r['value1'],
            "value2": r['value2'],
            "mode": r['mode'],
            "timestamp": r['timestamp']
        })
    return jsonify(readings)

if __name__ == '__main__':
    # Run locally on port 5000
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
