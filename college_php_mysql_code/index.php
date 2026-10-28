<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Green Building Performance Dashboard</title>
    <!-- Google Fonts: Inter and Outfit -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome for Iconography -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- html2pdf.js CDN for client-side PDF export -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <!-- Custom Style Sheet -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="logo-icon">
                    <i class="fa-solid fa-leaf text-glow-green"></i>
                </div>
                <div class="logo-text">
                    <h2>EcoBuild</h2>
                    <span>Green Building Dashboard</span>
                </div>
            </div>

            <nav class="sidebar-menu">
                <ul>
                    <li class="active" data-tab="dashboard">
                        <i class="fa-solid fa-chart-line"></i>
                        <span>Dashboard</span>
                    </li>
                    <li data-tab="alerts">
                        <i class="fa-solid fa-bell"></i>
                        <span>Live Alerts</span>
                        <span class="badge badge-danger alert-badge-count" id="badge-alerts-count">0</span>
                    </li>
                    <li data-tab="upload">
                        <i class="fa-solid fa-file-csv"></i>
                        <span>CSV Ingestion</span>
                    </li>
                    <li data-tab="settings">
                        <i class="fa-solid fa-gears"></i>
                        <span>Configurations</span>
                    </li>
                    <li data-tab="about">
                        <i class="fa-solid fa-circle-info"></i>
                        <span>System Architecture</span>
                    </li>
                </ul>
            </nav>

            <div class="sidebar-footer">
                <div class="user-profile" id="user-profile-section">
                    <div class="user-avatar">
                        <i class="fa-solid fa-user-lock"></i>
                    </div>
                    <div class="user-details">
                        <h4 id="profile-name">Guest View</h4>
                        <span id="profile-role">Limited Access</span>
                    </div>
                    <button class="auth-btn" id="login-trigger-btn" title="Admin Login">
                        <i class="fa-solid fa-right-to-bracket"></i>
                    </button>
                </div>
            </div>
        </aside>

        <!-- Main Display Window -->
        <main class="main-content" id="printable-area">
            <!-- Header -->
            <header class="main-header">
                <div class="header-title">
                    <h1 id="page-title">Ecological Analytics</h1>
                    <p class="timestamp-indicator">System Time: <span id="current-time-val">Loading...</span></p>
                </div>

                <div class="header-controls">
                    <!-- Master Toggle Status -->
                    <div class="mode-status-container">
                        <span class="mode-label">System Mode:</span>
                        <div class="mode-toggle-indicator" id="mode-indicator-pill">
                            <span class="pulse-indicator"></span>
                            <span id="mode-text">LIVE IoT MODE</span>
                        </div>
                    </div>

                    <!-- PDF Report Button -->
                    <button class="btn btn-primary" id="btn-export-pdf">
                        <i class="fa-solid fa-file-export"></i>
                        <span>Export Report</span>
                    </button>
                </div>
            </header>

            <!-- Dashboard View -->
            <section class="tab-panel active" id="tab-dashboard">
                <!-- Top Scoring and Overview Grid -->
                <div class="overview-grid">
                    <!-- Circular Score Progress Gauge -->
                    <div class="card card-score glow-green">
                        <div class="score-header">
                            <h3>Building Efficiency Score</h3>
                            <i class="fa-solid fa-shield-halved text-glow-green"></i>
                        </div>
                        <div class="gauge-container">
                            <div class="circular-progress">
                                <svg class="progress-ring" width="160" height="160">
                                    <circle class="progress-ring-circle-bg" stroke="rgba(255,255,255,0.05)" stroke-width="12" fill="transparent" r="70" cx="80" cy="80"/>
                                    <circle class="progress-ring-circle" id="building-score-circle" stroke="var(--neon-green)" stroke-width="12" fill="transparent" r="70" cx="80" cy="80" stroke-dasharray="439.8" stroke-dashoffset="439.8"/>
                                </svg>
                                <div class="score-value">
                                    <h1 id="val-building-score">0</h1>
                                    <span>/100</span>
                                </div>
                            </div>
                        </div>
                        <div class="score-footer">
                            <span class="score-grade" id="val-building-grade">Calculating...</span>
                            <p>Derived using ASHRAE 90.1 & LEED O+M Standards</p>
                        </div>
                    </div>

                    <!-- Metrics Grid -->
                    <div class="metrics-grid">
                        <!-- Energy Card -->
                        <div class="card card-metric glow-amber">
                            <div class="metric-icon bg-amber-trans">
                                <i class="fa-solid fa-bolt text-glow-amber"></i>
                            </div>
                            <div class="metric-data">
                                <span class="metric-label">Active Power Consumption</span>
                                <h2 class="metric-value"><span id="val-energy">0.0</span> <span class="metric-unit">W</span></h2>
                                <div class="metric-sub">
                                    <span class="sub-label">Current Node Score:</span>
                                    <span class="sub-value" id="score-energy">0/100</span>
                                </div>
                            </div>
                        </div>

                        <!-- Water Card -->
                        <div class="card card-metric glow-cyan">
                            <div class="metric-icon bg-cyan-trans">
                                <i class="fa-solid fa-droplet text-glow-cyan"></i>
                            </div>
                            <div class="metric-data">
                                <span class="metric-label">Water Flow Speed</span>
                                <h2 class="metric-value"><span id="val-water">0.0</span> <span class="metric-unit">L/min</span></h2>
                                <div class="metric-sub">
                                    <span class="sub-label">Current Node Score:</span>
                                    <span class="sub-value" id="score-water">0/100</span>
                                </div>
                            </div>
                        </div>

                        <!-- Climate Temp Card -->
                        <div class="card card-metric glow-violet">
                            <div class="metric-icon bg-violet-trans">
                                <i class="fa-solid fa-thermometer text-glow-violet"></i>
                            </div>
                            <div class="metric-data">
                                <span class="metric-label">Indoor Temperature</span>
                                <h2 class="metric-value"><span id="val-temp">0.0</span> <span class="metric-unit">°C</span></h2>
                                <div class="metric-sub">
                                    <span class="sub-label">Current Temp Score:</span>
                                    <span class="sub-value" id="score-climate">0/100</span>
                                </div>
                            </div>
                        </div>

                        <!-- Climate Humidity / Carbon Offset Card -->
                        <div class="card card-metric glow-green">
                            <div class="metric-icon bg-green-trans">
                                <i class="fa-solid fa-seedling text-glow-green"></i>
                            </div>
                            <div class="metric-data">
                                <span class="metric-label">Real-time Carbon Offset</span>
                                <h2 class="metric-value"><span id="val-carbon">0.0</span> <span class="metric-unit">kg CO₂</span></h2>
                                <div class="metric-sub">
                                    <span class="sub-label">Room Humidity:</span>
                                    <span class="sub-value" id="val-humidity">0.0%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Charts Visualization Section -->
                <div class="charts-section">
                    <div class="chart-container card glow-amber">
                        <div class="chart-header">
                            <h3><i class="fa-solid fa-bolt text-glow-amber mr-2"></i>Electrical Energy (PZEM-004T Node)</h3>
                            <span class="chart-unit">Unit: Watts (W)</span>
                        </div>
                        <div class="chart-body">
                            <canvas id="chart-energy"></canvas>
                        </div>
                    </div>

                    <div class="chart-container card glow-cyan">
                        <div class="chart-header">
                            <h3><i class="fa-solid fa-droplet text-glow-cyan mr-2"></i>Water Flow Rate (YF-S201 Node)</h3>
                            <span class="chart-unit">Unit: Liters / min (L/m)</span>
                        </div>
                        <div class="chart-body">
                            <canvas id="chart-water"></canvas>
                        </div>
                    </div>

                    <div class="chart-container card glow-violet" style="grid-column: span 2;">
                        <div class="chart-header">
                            <h3><i class="fa-solid fa-temperature-empty text-glow-violet mr-2"></i>Thermal comfort (DHT11 Server Room Climate)</h3>
                            <span class="chart-unit">Double axis: Temperature (°C) & Humidity (%)</span>
                        </div>
                        <div class="chart-body" style="height: 250px;">
                            <canvas id="chart-climate"></canvas>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Alerts View -->
            <section class="tab-panel" id="tab-alerts">
                <div class="card container-card">
                    <div class="card-header-actions">
                        <h2><i class="fa-solid fa-triangle-exclamation text-glow-red mr-2"></i>System Threshold Violations</h2>
                        <span class="table-info-counter" id="active-alerts-tag">0 Active Alerts</span>
                    </div>

                    <div class="table-container">
                        <table class="data-table" id="alerts-table">
                            <thead>
                                <tr>
                                    <th>Sensor Node</th>
                                    <th>Observed Reading</th>
                                    <th>Threshold Set</th>
                                    <th>Warning Message</th>
                                    <th>Occurred At</th>
                                    <th>Status</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="alerts-table-body">
                                <tr>
                                    <td colspan="7" class="text-center">No alerts recorded on this session.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- Upload View -->
            <section class="tab-panel" id="tab-upload">
                <div class="card container-card">
                    <h2><i class="fa-solid fa-file-excel text-glow-green mr-2"></i>Historical Baseline CSV Upload (Demo Mode)</h2>
                    <p class="description-text">
                        Upload custom building history data files to trigger "Demo Mode". The system will automatically parse historical time-series entries, calculate the scores for each record, and enable baseline audits.
                    </p>

                    <div class="upload-dropzone" id="csv-dropzone">
                        <i class="fa-solid fa-cloud-arrow-up upload-icon"></i>
                        <h3>Drag & drop your CSV file here</h3>
                        <p>or click to browse local files</p>
                        <input type="file" id="csv-file-input" accept=".csv" style="display: none;">
                        <span class="selected-file-label" id="csv-file-name">Supported format: .csv only</span>
                    </div>

                    <div class="csv-format-help">
                        <h4>Expected CSV Columns Structure:</h4>
                        <code>node_id, value1, value2, timestamp</code>

                        <div class="csv-example-box">
                            <h5>Sample CSV File Content:</h5>
                            <pre>node_id,value1,value2,timestamp
node_energy,2850.5,,2026-08-01 10:00:00
node_water,12.4,,2026-08-01 10:00:00
node_climate,24.5,55.0,2026-08-01 10:00:00
node_energy,3900.2,,2026-08-01 11:00:00</pre>
                        </div>
                    </div>

                    <button class="btn btn-success" id="btn-submit-csv" style="margin-top: 15px;" disabled>
                        <i class="fa-solid fa-square-check"></i>
                        <span>Start CSV Ingestion Process</span>
                    </button>
                </div>
            </section>

            <!-- Settings View -->
            <section class="tab-panel" id="tab-settings">
                <div class="settings-layout">
                    <!-- Auth Protected Overlay -->
                    <div class="auth-lock-overlay" id="settings-auth-overlay">
                        <i class="fa-solid fa-lock lock-icon"></i>
                        <h3>Calibration Lock Active</h3>
                        <p>You must authenticate as an Administrator to adjust sensor variables, thresholds, and operational mode.</p>
                        <button class="btn btn-primary" id="btn-settings-unlock">
                            <i class="fa-solid fa-key"></i>
                            <span>Authenticate Login</span>
                        </button>
                    </div>

                    <!-- Config Card -->
                    <div class="card container-card settings-form-container">
                        <h2><i class="fa-solid fa-sliders text-glow-cyan mr-2"></i>Calibration & Threshold Limits</h2>

                        <div class="settings-group">
                            <h3>Master Mode Selection</h3>
                            <div class="mode-selector-radio">
                                <label class="radio-label">
                                    <input type="radio" name="system_mode" value="LIVE" checked>
                                    <span class="custom-radio"></span>
                                    <div class="radio-text">
                                        <strong>Live IoT Streaming</strong>
                                        <p>Ingests real-time inputs streamed from ESP32 nodes over HTTP POST requests.</p>
                                    </div>
                                </label>
                                <label class="radio-label">
                                    <input type="radio" name="system_mode" value="DEMO">
                                    <span class="custom-radio"></span>
                                    <div class="radio-text">
                                        <strong>Demo & Historical CSV Mode</strong>
                                        <p>Renders visualizations and grading from uploaded legacy audit log spreadsheets.</p>
                                    </div>
                                </label>
                            </div>
                        </div>

                        <!-- Sensor Threshold Grid -->
                        <div class="settings-group">
                            <h3>Sensor Calibration Variables</h3>

                            <div class="sensor-config-rows">
                                <!-- Energy Sensor -->
                                <div class="sensor-config-item">
                                    <div class="sensor-title">
                                        <i class="fa-solid fa-bolt text-glow-amber"></i>
                                        <div>
                                            <strong>PZEM-004T (Energy Node)</strong>
                                            <p id="sensor-name-energy">Main Office Energy Node</p>
                                        </div>
                                    </div>
                                    <div class="sensor-inputs">
                                        <div class="input-field">
                                            <label>Alert Threshold (W)</label>
                                            <input type="number" id="input-thresh-energy" value="3500" step="100">
                                        </div>
                                        <div class="input-field">
                                            <label>Calibration Factor</label>
                                            <input type="number" id="input-cal-energy" value="1.00" step="0.05">
                                        </div>
                                    </div>
                                </div>

                                <!-- Water Sensor -->
                                <div class="sensor-config-item">
                                    <div class="sensor-title">
                                        <i class="fa-solid fa-droplet text-glow-cyan"></i>
                                        <div>
                                            <strong>YF-S201 (Water Flow Node)</strong>
                                            <p id="sensor-name-water">Ground Water Supply Line</p>
                                        </div>
                                    </div>
                                    <div class="sensor-inputs">
                                        <div class="input-field">
                                            <label>Alert Threshold (L/m)</label>
                                            <input type="number" id="input-thresh-water" value="25" step="1">
                                        </div>
                                        <div class="input-field">
                                            <label>Calibration Factor</label>
                                            <input type="number" id="input-cal-water" value="1.00" step="0.05">
                                        </div>
                                    </div>
                                </div>

                                <!-- Climate Sensor -->
                                <div class="sensor-config-item">
                                    <div class="sensor-title">
                                        <i class="fa-solid fa-temperature-half text-glow-violet"></i>
                                        <div>
                                            <strong>DHT11 (Climate Node)</strong>
                                            <p id="sensor-name-climate">Server Room Climate</p>
                                        </div>
                                    </div>
                                    <div class="sensor-inputs">
                                        <div class="input-field">
                                            <label>Temp Threshold (°C)</label>
                                            <input type="number" id="input-thresh-climate" value="28" step="1">
                                        </div>
                                        <div class="input-field">
                                            <label>Calibration Factor</label>
                                            <input type="number" id="input-cal-climate" value="1.00" step="0.05">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="settings-actions">
                            <button class="btn btn-primary" id="btn-save-settings">
                                <i class="fa-solid fa-floppy-disk"></i>
                                <span>Save Settings Configuration</span>
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- System Architecture & About View -->
            <section class="tab-panel" id="tab-about">
                <div class="card container-card">
                    <h2><i class="fa-solid fa-circle-info text-glow-green mr-2"></i>Interdisciplinary Project Architecture</h2>
                    <p class="subtitle-text">Convergence of Computer Science Engineering (CSE) and BCA Business Applications</p>

                    <div class="architecture-grid">
                        <div class="arch-col">
                            <h3><i class="fa-solid fa-microchip text-glow-amber mr-2"></i>CSE Focus (Hardware & Core Backend)</h3>
                            <ul>
                                <li><strong>Low-level Hardware Node:</strong> Microcontroller interface integration of PZEM-004T (Electrical load), YF-S201 (Flow velocity), and DHT11 (Thermal indices).</li>
                                <li><strong>Ingestion API (JSON):</strong> RESTful endpoint developed to ingest HTTP POST payloads streamed via ESP32 Wi-Fi modules securely.</li>
                                <li><strong>Data Persistence:</strong> MySQL database optimized for lightning-fast reads under continuous write loads.</li>
                                <li><strong>Mathematical Score Engine:</strong> Live computation logic evaluating complex metrics normalization against ASHRAE targets.</li>
                            </ul>
                        </div>
                        <div class="arch-col">
                            <h3><i class="fa-solid fa-chart-pie text-glow-cyan mr-2"></i>BCA Focus (Logic Flow & Business Auditing)</h3>
                            <ul>
                                <li><strong>Analytical UI Engine:</strong> High-performance frontend designed with vanilla CSS glassmorphism grids and responsive CSS transitions.</li>
                                <li><strong>Visual Rendering:</strong> Seamless integrations of Chart.js to map live dynamic line charts and double-axis layouts.</li>
                                <li><strong>Demo Data Parser:</strong> Client/server CSV ingestion tool to process historical data files for baseline carbon comparison.</li>
                                <li><strong>Compliance Auditor:</strong> Automated client-side PDF export system generating professional LEED documentation summaries.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="formula-section">
                        <h3><i class="fa-solid fa-calculator text-glow-violet mr-2"></i>Mathematical Formulation of Building Efficiency Score (BES)</h3>
                        <p class="formula-intro">The interdisciplinary scoring grade is calculated scientifically on a scale of 1–100 using environmental engineer targets:</p>

                        <div class="equation-box">
                            $$BES = 0.50 \times ES + 0.30 \times WS + 0.20 \times CS$$
                        </div>

                        <div class="formula-variables">
                            <div class="var-item">
                                <strong>ES (Energy Score)</strong>
                                <p>Normalizes current Active Power (W) against user-defined alert thresholds. Drops progressively when threshold is violated to represent higher carbon loading.</p>
                            </div>
                            <div class="var-item">
                                <strong>WS (Water Score)</strong>
                                <p>Normalizes current water flow speed (L/m) against limit thresholds. Measures utility performance and flags continuous leakage patterns.</p>
                            </div>
                            <div class="var-item">
                                <strong>CS (Climate Score)</strong>
                                <p>Evaluates Thermal Comfort Indices (Temperature & Humidity) using ASHRAE Standard 55 thermal comfort ranges (Ideal Temp: 20°C-25°C, Humidity: 30%-60%). Deviations trigger penalty calculations.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <!-- Login Modal -->
    <div class="modal-backdrop" id="login-modal">
        <div class="modal card glow-green">
            <div class="modal-header">
                <h3><i class="fa-solid fa-user-shield text-glow-green mr-2"></i>Admin Authentication</h3>
                <button class="modal-close-btn" id="login-modal-close"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <form id="login-form">
                <div class="modal-body">
                    <div class="alert alert-danger" id="login-error-msg" style="display: none;">
                        Invalid admin credentials. Please try again.
                    </div>
                    <div class="form-field">
                        <label for="login-username"><i class="fa-solid fa-user mr-1"></i>Username</label>
                        <input type="text" id="login-username" required placeholder="Enter admin username" value="admin">
                    </div>
                    <div class="form-field">
                        <label for="login-password"><i class="fa-solid fa-key mr-1"></i>Password</label>
                        <input type="password" id="login-password" required placeholder="Enter password" value="admin123">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" id="login-cancel-btn">Cancel</button>
                    <button type="submit" class="btn btn-success">Authenticate</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MathJax for rendering LaTeX formulas -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <!-- JavaScript Controller -->
    <script src="app.js"></script>
</body>
</html>
