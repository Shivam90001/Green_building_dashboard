# Green Building Performance Dashboard (Dual Mode)

A premium, state-of-the-art college final year project representing the convergence of **Computer Science Engineering (CSE)** and **BCA Business Information Systems**.

This repository contains two complete implementations:
1. **Desktop App Edition (Python & SQLite)**: A local version running on your PC, launched via a custom Desktop shortcut. It runs a backend Flask server, uses a self-contained SQLite database, and features a responsive dashboard UI.
2. **College Submission Edition (PHP & MySQL)**: Located in the `college_php_mysql_code/` directory, designed for hosting on a local server like XAMPP to match your project documentation perfectly.

---

## Key Features

- **Dual-Mode Data Acquisition**: Seamlessly toggle between **Live IoT Mode** (real-time HTTP POST JSON payloads) and **Demo/Historical Mode** (CSV spreadsheet parsing).
- **Interdisciplinary Scoring Algorithm**: Computes a scientific **Building Efficiency Score (1-100)** derived from ASHRAE 55 and LEED v4.1 criteria:
  $$BES = 0.50 \times Energy\_Score + 0.30 \times Water\_Score + 0.20 \times Climate\_Score$$
- **Hardware Integration Simulation**: Python mock script simulating ESP32 microcontrollers streaming PZEM-004T (energy), YF-S201 (water), and DHT11 (temperature & humidity) logs.
- **Glassmorphic Analytical UI**: Highly responsive web frontend featuring floating frosted-glass panels, interactive metric scales, and real-time Chart.js line charts.
- **Compliance Auditor**: Native PDF rendering script exporting dynamic reports and active charts.
- **Admin Configuration Security**: Encrypted administrative lock to prevent unauthorized calibration changes.

---

## Desktop App Edition: Setup & Run

### 1. Install Python Dependencies
Open a command prompt in the project directory and run:
```cmd
py -m pip install -r requirements.txt
```

### 2. Launch the Server and Web UI
Simply double-click the **"Green Building Dashboard"** icon on your Desktop!

Alternatively, you can run the launcher manually:
1. Open a command prompt and navigate to the project directory.
2. Run the launcher script:
   ```cmd
   launcher\start_dashboard.bat
   ```
This starts the Flask server on port 5000 in a separate console and opens the interface in a standalone window. Close the `EcoBuildServer` console to stop the server.

### 3. Simulate ESP32 IoT Nodes
To demonstrate **Live IoT Mode** running with real-time data:
1. Open another command prompt in the project folder.
2. Run the simulator script:
   ```cmd
   py mock_iot\esp32_simulator.py
   ```
The simulator will immediately start streaming realistic readings (representing energy, water, and climate) to your dashboard every 5 seconds. You will see the metrics and charts update live!

### 4. Log In as Administrator
To adjust alert thresholds or modify calibration parameters:
1. Click the lock/login icon in the bottom-left sidebar.
2. Enter the default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

---

## College Submission Edition: Setup in XAMPP
The code files matching the documentation are located in `college_php_mysql_code/`.

To host them in XAMPP:
1. Copy the files inside `college_php_mysql_code/` to `C:\xampp\htdocs\green_building_dashboard\`.
2. Turn on Apache and MySQL in XAMPP.
3. Import the `database.sql` file in phpMyAdmin (`http://localhost/phpmyadmin`).
4. Open the browser and visit `http://localhost/green_building_dashboard/`.

*See `college_php_mysql_code/readme_college.txt` for more detailed instructions.*
