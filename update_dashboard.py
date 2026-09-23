# -*- coding: utf-8 -*-
import os
import shutil
import sys
import subprocess

SRC_DIR = r"C:\Users\abc\.gemini\antigravity\scratch\green_building_dashboard"
DEST_DIR = r"C:\Users\abc\green building dashboard"

# 1. New HTML Content
INDEX_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
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
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="sidebar-overlay" id="sidebar-overlay"></div>

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
                    <li data-tab="leed">
                        <i class="fa-solid fa-square-check"></i>
                        <span>LEED Certifier</span>
                    </li>
                    <li data-tab="logs">
                        <i class="fa-solid fa-database"></i>
                        <span>Data Logs</span>
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
                <div class="header-left-section">
                    <button class="mobile-nav-toggle" id="btn-mobile-toggle" aria-label="Toggle Navigation">
                        <i class="fa-solid fa-bars"></i>
                    </button>
                    <div class="header-title">
                        <h1 id="page-title">Ecological Analytics</h1>
                        <p class="timestamp-indicator">System Time: <span id="current-time-val">Loading...</span></p>
                    </div>
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

                    <!-- Fullscreen Toggle Button -->
                    <button class="btn btn-secondary btn-fullscreen" id="btn-toggle-fullscreen" title="Toggle Fullscreen">
                        <i class="fa-solid fa-expand"></i>
                        <span>Fullscreen</span>
                    </button>
                    
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
                                    <circle class="progress-ring-circle-bg" stroke="rgba(0,0,0,0.06)" stroke-width="12" fill="transparent" r="70" cx="80" cy="80"/>
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
                                <span class="metric-label">Water Flow Velocity</span>
                                <h2 class="metric-value"><span id="val-water">0.0</span> <span class="metric-unit">L/m</span></h2>
                                <div class="metric-sub">
                                    <span class="sub-label">Current Node Score:</span>
                                    <span class="sub-value" id="score-water">0/100</span>
                                </div>
                            </div>
                        </div>

                        <!-- Climate Temp Card -->
                        <div class="card card-metric glow-violet">
                            <div class="metric-icon bg-violet-trans">
                                <i class="fa-solid fa-temperature-three-quarters text-glow-violet"></i>
                            </div>
                            <div class="metric-data">
                                <span class="metric-label">Indoor Temperature</span>
                                <h2 class="metric-value"><span id="val-temp">0.0</span> <span class="metric-unit">&deg;C</span></h2>
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
                                <h2 class="metric-value"><span id="val-carbon">0.0</span> <span class="metric-unit">kg CO<sub>2</sub></span></h2>
                                <div class="metric-sub">
                                    <span class="sub-label">Room Humidity:</span>
                                    <span class="sub-value" id="val-humidity">0.0%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Active Goals Tracker Card -->
                <div class="card container-card glow-green" style="margin-bottom: 24px;">
                    <div class="card-header-actions">
                        <h2><i class="fa-solid fa-bullseye text-glow-green mr-2"></i>Active Sustainability Goals</h2>
                        <span class="table-info-counter" id="goal-status-badge" style="background: rgba(16, 185, 129, 0.1); color: var(--neon-green); border-color: rgba(16, 185, 129, 0.2);">On Track</span>
                    </div>
                    <div class="goals-grid">
                        <div class="goal-item-box" style="background: rgba(0,0,0,0.02); padding: 18px; border-radius: 12px; border: 1px solid var(--glass-border);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <strong><i class="fa-solid fa-bolt text-glow-amber mr-1"></i>Energy Saving Goal</strong>
                                <span id="energy-goal-text">Limit: 3000 W</span>
                            </div>
                            <div class="progress-bar-container" style="background: rgba(0,0,0,0.05); height: 10px; border-radius: 6px; overflow: hidden;">
                                <div id="energy-goal-progress" style="background: var(--neon-amber); width: 0%; height: 100%; transition: width 0.5s;"></div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-secondary); margin-top: 8px;">
                                <span>Current: <span id="energy-goal-curr">0 W</span></span>
                                <span id="energy-goal-pct">0% used</span>
                            </div>
                        </div>

                        <div class="goal-item-box" style="background: rgba(0,0,0,0.02); padding: 18px; border-radius: 12px; border: 1px solid var(--glass-border);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <strong><i class="fa-solid fa-droplet text-glow-cyan mr-1"></i>Water Conservation Goal</strong>
                                <span id="water-goal-text">Limit: 20 L/m</span>
                            </div>
                            <div class="progress-bar-container" style="background: rgba(0,0,0,0.05); height: 10px; border-radius: 6px; overflow: hidden;">
                                <div id="water-goal-progress" style="background: var(--neon-cyan); width: 0%; height: 100%; transition: width 0.5s;"></div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-secondary); margin-top: 8px;">
                                <span>Current: <span id="water-goal-curr">0 L/m</span></span>
                                <span id="water-goal-pct">0% used</span>
                            </div>
                        </div>

                        <div class="goal-item-box" style="background: rgba(0,0,0,0.02); padding: 18px; border-radius: 12px; border: 1px solid var(--glass-border); display: flex; flex-direction: column; justify-content: center; text-align: center;">
                            <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 6px;">Ecological Impact Highlight</h4>
                            <p style="font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4;">
                                Active carbon saving equivalent to planting <strong id="val-trees" style="color: var(--neon-green);">0.0</strong> mature trees today!
                            </p>
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

                    <div class="chart-container card glow-violet full-width">
                        <div class="chart-header">
                            <h3><i class="fa-solid fa-temperature-half text-glow-violet mr-2"></i>Thermal Comfort (DHT11 Server Room Climate)</h3>
                            <span class="chart-unit">Double axis: Temperature (&deg;C) & Humidity (%)</span>
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
                        <h2><i class="fa-solid fa-triangle-exclamation text-glow-red mr-2"></i>Real-time Anomaly Alerts</h2>
                        <span class="table-info-counter" id="active-alerts-tag">0 Active Anomalies</span>
                    </div>
                    <div class="table-container">
                        <table class="data-table" id="alerts-table">
                            <thead>
                                <tr>
                                    <th>Severity</th>
                                    <th>Node ID</th>
                                    <th>Metric Value</th>
                                    <th>Threshold</th>
                                    <th>Time Detected</th>
                                    <th>Status</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="alerts-tbody">
                                <tr>
                                    <td colspan="7" class="text-center">No anomalies registered. Systems functioning normally.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- CSV Upload View -->
            <section class="tab-panel" id="tab-upload">
                <div class="card container-card">
                    <h2><i class="fa-solid fa-file-arrow-up text-glow-cyan mr-2"></i>Batch CSV Data Ingestion & Audit</h2>
                    <p class="description-text">
                        Upload historical sensor time-series datasets to populate analytics tables, test machine learning score weights, and conduct baseline comparisons.
                    </p>

                    <div class="upload-dropzone" id="csv-dropzone">
                        <i class="fa-solid fa-cloud-arrow-up upload-icon"></i>
                        <h3>Drag and Drop your CSV dataset here</h3>
                        <p>Supported standard schema: PZEM, YF-S201, and DHT11 time-series logs</p>
                        <span class="selected-file-label" id="csv-file-name">No file selected</span>
                        <input type="file" id="csv-file-input" accept=".csv" style="display: none;">
                    </div>

                    <div class="csv-format-help">
                        <h4>Expected CSV Header Column Format:</h4>
                        <code>node_id, value1, value2, timestamp</code>
                        <div class="csv-example-box">
                            <h5>Sample Structure:</h5>
                            <pre>node_id,value1,value2,timestamp
node_energy,2850.5,,2026-08-01 10:00:00
node_water,12.4,,2026-08-01 10:00:00
node_climate,24.5,55.0,2026-08-01 10:00:00
node_energy,3900.2,,2026-08-01 11:00:00</pre>
                        </div>
                    </div>
                    
                    <button class="btn btn-success" id="btn-submit-csv" style="margin-top: 20px;" disabled>
                        <i class="fa-solid fa-square-check"></i>
                        <span>Start CSV Ingestion Process</span>
                    </button>
                </div>
            </section>

            <!-- LEED Sustainability Certifier View -->
            <section class="tab-panel" id="tab-leed">
                <div class="card container-card">
                    <div class="card-header-actions">
                        <h2><i class="fa-solid fa-medal text-glow-green mr-2"></i>LEED v4.1 Building Certifier</h2>
                        <div class="leed-badge-container">
                            <span class="table-info-counter" id="val-leed-grade" style="background: rgba(16, 185, 129, 0.1); color: var(--neon-green); border-color: rgba(16, 185, 129, 0.2); font-size: 0.95rem; font-weight: 700; padding: 8px 18px;">LEED Certified (0 Points)</span>
                        </div>
                    </div>
                    <p class="description-text">
                        Select the sustainable design criteria met by the building to calculate its real-time LEED score and target rating.
                    </p>

                    <div class="leed-grid">
                        <!-- Category 1: Energy & Atmosphere -->
                        <div class="card" style="background: rgba(0,0,0,0.01); border: 1px solid var(--glass-border);">
                            <h3 style="font-size: 1.1rem; color: var(--neon-amber); margin-bottom: 15px;"><i class="fa-solid fa-solar-panel mr-2"></i>Energy & Atmosphere</h3>
                            <div style="display: flex; flex-direction: column; gap: 12px;">
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="15" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Solar PV Panels installed (15 pts)</span>
                                </label>
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="10" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>High-efficiency Energy Star HVAC (10 pts)</span>
                                </label>
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="10" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Smart sensor LED lighting system (10 pts)</span>
                                </label>
                            </div>
                        </div>

                        <!-- Category 2: Water Efficiency -->
                        <div class="card" style="background: rgba(0,0,0,0.01); border: 1px solid var(--glass-border);">
                            <h3 style="font-size: 1.1rem; color: var(--neon-cyan); margin-bottom: 15px;"><i class="fa-solid fa-sink mr-2"></i>Water Efficiency</h3>
                            <div style="display: flex; flex-direction: column; gap: 12px;">
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="15" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Rainwater Harvesting & Storage (15 pts)</span>
                                </label>
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="10" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Graywater Recycling & Reuse System (10 pts)</span>
                                </label>
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="5" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Low-flow toilets & faucets (5 pts)</span>
                                </label>
                            </div>
                        </div>

                        <!-- Category 3: Materials & Resources -->
                        <div class="card" style="background: rgba(0,0,0,0.01); border: 1px solid var(--glass-border);">
                            <h3 style="font-size: 1.1rem; color: var(--neon-green); margin-bottom: 15px;"><i class="fa-solid fa-recycle mr-2"></i>Materials & Resources</h3>
                            <div style="display: flex; flex-direction: column; gap: 12px;">
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="10" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Eco-friendly / Recycled materials (10 pts)</span>
                                </label>
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="10" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Waste segregation & on-site composting (10 pts)</span>
                                </label>
                            </div>
                        </div>

                        <!-- Category 4: Indoor Environmental Quality -->
                        <div class="card" style="background: rgba(0,0,0,0.01); border: 1px solid var(--glass-border);">
                            <h3 style="font-size: 1.1rem; color: var(--neon-violet); margin-bottom: 15px;"><i class="fa-solid fa-wind mr-2"></i>Indoor Environment</h3>
                            <div style="display: flex; flex-direction: column; gap: 12px;">
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="10" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Low VOC emissions paint & furniture (10 pts)</span>
                                </label>
                                <label class="checkbox-label" style="display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 0.85rem;">
                                    <input type="checkbox" class="leed-checkbox" value="5" style="width: 18px; height: 18px; cursor: pointer;">
                                    <span>Optimized natural daylighting design (5 pts)</span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Data Logs Explorer View -->
            <section class="tab-panel" id="tab-logs">
                <div class="card container-card">
                    <div class="card-header-actions">
                        <h2><i class="fa-solid fa-database text-glow-cyan mr-2"></i>Persistent IoT Time-Series Database</h2>
                        <button class="btn btn-secondary" id="btn-refresh-logs">
                            <i class="fa-solid fa-rotate"></i>
                            <span>Refresh Logs</span>
                        </button>
                    </div>
                    <div class="table-container">
                        <table class="data-table" id="logs-table">
                            <thead>
                                <tr>
                                    <th>Log ID</th>
                                    <th>Sensor Node</th>
                                    <th>Primary Reading</th>
                                    <th>Secondary Reading</th>
                                    <th>Normalized Score</th>
                                    <th>Timestamp</th>
                                </tr>
                            </thead>
                            <tbody id="logs-tbody">
                                <tr>
                                    <td colspan="6" class="text-center">Loading database telemetry records...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- Configuration / Settings View -->
            <section class="tab-panel" id="tab-settings">
                <div class="card container-card settings-layout">
                    <!-- Authentication Lock Overlay -->
                    <div class="auth-lock-overlay" id="settings-auth-overlay">
                        <i class="fa-solid fa-lock lock-icon"></i>
                        <h3>Restricted Access</h3>
                        <p>Calibration controls and sensor thresholds are locked. Please authenticate with administrator credentials.</p>
                        <button class="btn btn-primary" id="btn-settings-unlock">
                            <i class="fa-solid fa-key"></i>
                            <span>Authenticate as Administrator</span>
                        </button>
                    </div>

                    <!-- Protected Settings Content -->
                    <div class="settings-content" id="settings-form-wrapper">
                        <h2><i class="fa-solid fa-sliders text-glow-cyan mr-2"></i>System Thresholds & IoT Mode</h2>
                        <p class="description-text">Calibrate sensor thresholds, toggle live hardware integration vs demo mode, and configure alerts.</p>
                        
                        <div class="settings-group">
                            <h3>Operating Mode</h3>
                            <div class="mode-selector-radio">
                                <label class="radio-label">
                                    <input type="radio" name="system-mode" value="live" id="mode-live" checked>
                                    <span class="custom-radio"></span>
                                    <div class="radio-text">
                                        <strong>Live IoT Hardware Ingestion</strong>
                                        <p>Receives real HTTP POST telemetry payloads from connected ESP32 microcontrollers.</p>
                                    </div>
                                </label>
                                <label class="radio-label">
                                    <input type="radio" name="system-mode" value="demo" id="mode-demo">
                                    <span class="custom-radio"></span>
                                    <div class="radio-text">
                                        <strong>Interactive Demo Simulation</strong>
                                        <p>Generates realistic continuous building telemetry data automatically for testing.</p>
                                    </div>
                                </label>
                            </div>
                        </div>

                        <div class="settings-group">
                            <h3>Sensor Calibration & Alert Triggers</h3>
                            <div class="sensor-config-rows">
                                <div class="sensor-config-item">
                                    <div class="sensor-title">
                                        <i class="fa-solid fa-bolt text-glow-amber"></i>
                                        <div>
                                            <strong>PZEM-004T (Electrical Node)</strong>
                                            <p id="sensor-name-energy">Main Floor Power Meter</p>
                                        </div>
                                    </div>
                                    <div class="sensor-inputs">
                                        <div class="input-field">
                                            <label>Alert Threshold (W)</label>
                                            <input type="number" id="input-thresh-energy" value="3500" step="50">
                                        </div>
                                        <div class="input-field">
                                            <label>Calibration Factor</label>
                                            <input type="number" id="input-cal-energy" value="1.00" step="0.05">
                                        </div>
                                    </div>
                                </div>

                                <div class="sensor-config-item">
                                    <div class="sensor-title">
                                        <i class="fa-solid fa-droplet text-glow-cyan"></i>
                                        <div>
                                            <strong>YF-S201 (Flow Node)</strong>
                                            <p id="sensor-name-water">Main Water Supply Line</p>
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
                                            <label>Temp Threshold (&deg;C)</label>
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
                                <li><strong>Data Persistence:</strong> SQLite3 time-series database optimized for lightning-fast reads under continuous write loads.</li>
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
                        <p class="formula-intro">The interdisciplinary scoring grade is calculated scientifically on a scale of 1 &ndash; 100 using environmental engineer targets:</p>
                        
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
                                <p>Evaluates Thermal Comfort Indices (Temperature & Humidity) using ASHRAE Standard 55 thermal comfort ranges (Ideal Temp: 20&deg;C&ndash;25&deg;C, Humidity: 30%&ndash;60%). Deviations trigger penalty calculations.</p>
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
    <script src="js/app.js"></script>
</body>
</html>'''

# 2. New CSS Content
STYLE_CSS = r'''/* Root Color Variables & Modern Light Theme Design System */
:root {
    --bg-primary: #f8fafc;
    --bg-secondary: #ffffff;
    --glass-bg: rgba(255, 255, 255, 0.92);
    --glass-border: rgba(226, 232, 240, 0.9);
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    
    /* Neon Colors adapted for light mode */
    --neon-green: #059669;
    --neon-green-glow: rgba(5, 150, 105, 0.2);
    --neon-amber: #d97706;
    --neon-amber-glow: rgba(217, 119, 6, 0.2);
    --neon-cyan: #0891b2;
    --neon-cyan-glow: rgba(8, 145, 178, 0.2);
    --neon-violet: #7c3aed;
    --neon-violet-glow: rgba(124, 58, 237, 0.2);
    --neon-red: #dc2626;
    --neon-red-glow: rgba(220, 38, 38, 0.2);
    
    /* System Shadows & Typography */
    --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.03);
    --font-heading: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Global Reset & Box Sizing */
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    font-size: 16px;
    width: 100%;
    height: 100%;
    scroll-behavior: smooth;
}

body {
    width: 100%;
    min-height: 100vh;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    background-color: var(--bg-primary);
    background-image: 
        radial-gradient(at 10% 20%, rgba(124, 58, 237, 0.04) 0px, transparent 50%),
        radial-gradient(at 90% 10%, rgba(8, 145, 178, 0.04) 0px, transparent 50%),
        radial-gradient(at 50% 80%, rgba(5, 150, 105, 0.04) 0px, transparent 50%);
    color: var(--text-primary);
    font-family: var(--font-body);
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
    letter-spacing: -0.3px;
    color: var(--text-primary);
}

/* App Container Layout */
.app-container {
    display: flex;
    width: 100%;
    max-width: 100%;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

/* Sidebar Navigation */
.sidebar {
    width: 260px;
    min-width: 260px;
    max-width: 260px;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 100;
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-right: 1px solid var(--glass-border);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24px 16px;
    overflow-y: auto;
    overflow-x: hidden;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.03);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    padding: 0 8px;
}

.logo-icon {
    font-size: 1.8rem;
}

.logo-text h2 {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.1;
}

.logo-text span {
    font-size: 0.7rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
}

.sidebar-menu {
    flex: 1 1 auto;
}

.sidebar-menu ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.sidebar-menu li {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 10px;
    color: var(--text-secondary);
    cursor: pointer;
    font-weight: 500;
    font-size: 0.88rem;
    transition: all 0.2s ease;
    border: 1px solid transparent;
    position: relative;
}

.sidebar-menu li i {
    font-size: 1.05rem;
    width: 22px;
    text-align: center;
}

.sidebar-menu li:hover {
    color: var(--text-primary);
    background: rgba(0, 0, 0, 0.03);
    transform: translateX(3px);
}

.sidebar-menu li.active {
    color: var(--neon-green);
    background: rgba(5, 150, 105, 0.08);
    border-color: rgba(5, 150, 105, 0.18);
    font-weight: 600;
}

.sidebar-menu li.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 15%;
    height: 70%;
    width: 3px;
    background: var(--neon-green);
    border-radius: 0 3px 3px 0;
}

.badge {
    padding: 2px 7px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    margin-left: auto;
}

.badge-danger {
    background: var(--neon-red);
    color: white;
}

/* Sidebar Profile Footer */
.sidebar-footer {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--glass-border);
}

.user-profile {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    background: rgba(0, 0, 0, 0.02);
    border-radius: 10px;
    border: 1px solid rgba(0, 0, 0, 0.04);
}

.user-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    font-size: 0.85rem;
}

.user-details {
    flex-grow: 1;
    overflow: hidden;
}

.user-details h4 {
    font-size: 0.82rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.user-details span {
    font-size: 0.7rem;
    color: var(--text-secondary);
    display: block;
}

.auth-btn {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 1rem;
    padding: 4px;
    transition: color 0.2s;
}

.auth-btn:hover {
    color: var(--neon-green);
}

/* Main Content Area */
.main-content {
    margin-left: 260px;
    width: calc(100% - 260px);
    max-width: calc(100% - 260px);
    min-width: 0;
    min-height: 100vh;
    padding: clamp(16px, 2.5vw, 32px);
    box-sizing: border-box;
    overflow-x: hidden;
}

/* Main Header */
.main-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 24px;
    width: 100%;
}

.header-left-section {
    display: flex;
    align-items: center;
    gap: 12px;
}

.mobile-nav-toggle {
    display: none;
    background: #ffffff;
    border: 1px solid var(--glass-border);
    color: var(--text-primary);
    font-size: 1.15rem;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    cursor: pointer;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    transition: all 0.2s;
}

.mobile-nav-toggle:hover {
    background: #f1f5f9;
}

.header-title h1 {
    font-size: clamp(1.4rem, 2.2vw, 2rem);
    font-weight: 800;
    margin-bottom: 2px;
    background: linear-gradient(135deg, #0f172a 40%, #334155 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.timestamp-indicator {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.header-controls {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}

.mode-status-container {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.85);
    padding: 6px 14px;
    border-radius: 30px;
    border: 1px solid var(--glass-border);
}

.mode-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-weight: 600;
    text-transform: uppercase;
}

.mode-toggle-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    background: rgba(5, 150, 105, 0.08);
    color: var(--neon-green);
    border: 1px solid rgba(5, 150, 105, 0.2);
}

.mode-toggle-indicator.demo-mode {
    background: rgba(217, 119, 6, 0.08);
    color: var(--neon-amber);
    border: 1px solid rgba(217, 119, 6, 0.2);
}

.pulse-indicator {
    width: 6px;
    height: 6px;
    background: currentColor;
    border-radius: 50%;
    animation: pulse 1.8s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.9); opacity: 0.6; }
    50% { transform: scale(1.4); opacity: 1; }
    100% { transform: scale(0.9); opacity: 0.6; }
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 9px 16px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    font-family: var(--font-heading);
    border: 1px solid transparent;
    text-decoration: none;
    white-space: nowrap;
}

.btn-primary {
    background: #0891b2;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(8, 145, 178, 0.2);
}

.btn-primary:hover {
    background: #0e7490;
    transform: translateY(-1px);
}

.btn-success {
    background: #059669;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.2);
}

.btn-success:hover:not(:disabled) {
    background: #047857;
    transform: translateY(-1px);
}

.btn-secondary {
    background: #ffffff;
    color: var(--text-primary);
    border: 1px solid var(--glass-border);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.btn-secondary:hover {
    background: #f1f5f9;
    border-color: #cbd5e1;
    transform: translateY(-1px);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Cards System */
.card {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 20px;
    box-shadow: var(--card-shadow);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dashboard Tab Panel Layout */
.tab-panel {
    display: none;
    width: 100%;
}

.tab-panel.active {
    display: block;
    animation: fadeIn 0.35s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Overview Layout Grid */
.overview-grid {
    display: grid;
    grid-template-columns: minmax(270px, 320px) minmax(0, 1fr);
    gap: 20px;
    margin-bottom: 24px;
    width: 100%;
}

/* Score Card */
.card-score {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    text-align: center;
    background: radial-gradient(circle at top right, rgba(5, 150, 105, 0.05), transparent 70%), var(--glass-bg);
}

.score-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 12px;
}

.score-header h3 {
    font-size: 0.95rem;
    color: var(--text-secondary);
    font-weight: 600;
}

.gauge-container {
    position: relative;
    width: 160px;
    height: 160px;
    margin: 12px 0;
}

.circular-progress {
    position: relative;
    width: 100%;
    height: 100%;
}

.progress-ring {
    transform: rotate(-90deg);
}

.progress-ring-circle {
    transition: stroke-dashoffset 0.6s ease;
}

.score-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    align-items: baseline;
    justify-content: center;
}

.score-value h1 {
    font-size: 3rem;
    font-weight: 800;
    font-family: var(--font-heading);
}

.score-value span {
    font-size: 1rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.score-footer {
    width: 100%;
    margin-top: 12px;
}

.score-grade {
    display: inline-block;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--neon-green);
    margin-bottom: 4px;
}

.score-footer p {
    font-size: 0.72rem;
    color: var(--text-secondary);
    line-height: 1.3;
}

/* Metrics Cards Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    width: 100%;
}

.card-metric {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 18px 20px;
    min-width: 0;
}

.metric-icon {
    width: 50px;
    height: 50px;
    min-width: 50px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    border: 1px solid rgba(0, 0, 0, 0.04);
}

.bg-amber-trans { background: rgba(217, 119, 6, 0.08); color: var(--neon-amber); border-color: rgba(217, 119, 6, 0.2) !important; }
.bg-cyan-trans { background: rgba(8, 145, 178, 0.08); color: var(--neon-cyan); border-color: rgba(8, 145, 178, 0.2) !important; }
.bg-violet-trans { background: rgba(124, 58, 237, 0.08); color: var(--neon-violet); border-color: rgba(124, 58, 237, 0.2) !important; }
.bg-green-trans { background: rgba(5, 150, 105, 0.08); color: var(--neon-green); border-color: rgba(5, 150, 105, 0.2) !important; }

.metric-data {
    flex: 1 1 auto;
    min-width: 0;
    overflow: hidden;
}

.metric-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-weight: 500;
    display: block;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.metric-value {
    font-size: clamp(1.4rem, 1.8vw, 1.75rem);
    font-weight: 700;
    font-family: var(--font-heading);
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.metric-unit {
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.metric-sub {
    font-size: 0.72rem;
    display: flex;
    gap: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sub-label {
    color: var(--text-secondary);
}

.sub-value {
    font-weight: 700;
    color: var(--text-primary);
}

/* Goals Grid */
.goals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
    margin-top: 15px;
    width: 100%;
}

/* Charts Grid Section */
.charts-section {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
    width: 100%;
}

.chart-container {
    min-height: 300px;
    width: 100%;
    min-width: 0;
}

.chart-container.full-width {
    grid-column: 1 / -1;
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 8px;
}

.chart-header h3 {
    font-size: 0.95rem;
    font-weight: 600;
    display: flex;
    align-items: center;
}

.chart-unit {
    font-size: 0.72rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.chart-body {
    position: relative;
    height: 230px;
    width: 100%;
    min-width: 0;
}

/* Tables CSS */
.container-card {
    background: var(--glass-bg);
}

.card-header-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--glass-border);
}

.card-header-actions h2 {
    font-size: 1.25rem;
    font-weight: 700;
}

.table-info-counter {
    background: rgba(220, 38, 38, 0.1);
    color: var(--neon-red);
    border: 1px solid rgba(220, 38, 38, 0.2);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
}

.table-container {
    width: 100%;
    max-width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border-radius: 12px;
    border: 1px solid var(--glass-border);
}

.data-table {
    width: 100%;
    min-width: 600px;
    border-collapse: collapse;
    text-align: left;
}

.data-table th {
    background: #f1f5f9;
    padding: 12px 16px;
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--glass-border);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.data-table td {
    padding: 12px 16px;
    font-size: 0.84rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.04);
    color: var(--text-primary);
}

.data-table tbody tr:hover {
    background: rgba(0, 0, 0, 0.015);
}

.text-center {
    text-align: center;
}

.badge-outline-danger {
    background: rgba(220, 38, 38, 0.08);
    color: var(--neon-red);
    border: 1px solid rgba(220, 38, 38, 0.25);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
}

.badge-outline-success {
    background: rgba(5, 150, 105, 0.08);
    color: var(--neon-green);
    border: 1px solid rgba(5, 150, 105, 0.25);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
}

.action-link-btn {
    background: transparent;
    border: none;
    color: var(--neon-cyan);
    cursor: pointer;
    font-weight: 600;
    font-size: 0.82rem;
}

.action-link-btn:hover {
    text-decoration: underline;
}

/* Upload Page CSS */
.description-text {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: 24px;
    line-height: 1.5;
}

.upload-dropzone {
    border: 2px dashed #cbd5e1;
    background: #f8fafc;
    border-radius: 14px;
    padding: 40px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 24px;
}

.upload-dropzone:hover, .upload-dropzone.dragover {
    border-color: var(--neon-green);
    background: rgba(5, 150, 105, 0.02);
}

.upload-icon {
    font-size: 2.5rem;
    color: var(--text-secondary);
    margin-bottom: 14px;
}

.upload-dropzone:hover .upload-icon {
    color: var(--neon-green);
}

.upload-dropzone h3 {
    font-size: 1.1rem;
    margin-bottom: 6px;
}

.upload-dropzone p {
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-bottom: 10px;
}

.selected-file-label {
    display: inline-block;
    font-size: 0.78rem;
    padding: 4px 12px;
    background: #e2e8f0;
    border-radius: 6px;
    color: var(--text-secondary);
}

.upload-dropzone.has-file .selected-file-label {
    background: rgba(5, 150, 105, 0.1);
    color: var(--neon-green);
    border: 1px solid rgba(5, 150, 105, 0.2);
    font-weight: 600;
}

.csv-format-help {
    background: #f8fafc;
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 16px;
}

.csv-format-help h4 {
    font-size: 0.9rem;
    margin-bottom: 8px;
    font-weight: 600;
}

.csv-format-help code {
    display: inline-block;
    padding: 4px 8px;
    background: #ffffff;
    color: var(--neon-violet);
    font-family: monospace;
    font-size: 0.82rem;
    border: 1px solid var(--glass-border);
    border-radius: 4px;
    margin-bottom: 16px;
}

.csv-example-box h5 {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-bottom: 6px;
}

.csv-example-box pre {
    background: #ffffff;
    color: #334155;
    padding: 12px;
    border-radius: 8px;
    font-family: monospace;
    font-size: 0.78rem;
    overflow-x: auto;
    border: 1px solid var(--glass-border);
}

/* LEED Grid */
.leed-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
    margin-top: 20px;
    width: 100%;
}

/* Settings Form UI */
.settings-layout {
    position: relative;
    min-height: 400px;
}

.auth-lock-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(248, 250, 252, 0.95);
    backdrop-filter: blur(8px);
    z-index: 5;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    border: 1px solid var(--glass-border);
    text-align: center;
    padding: 20px;
}

.lock-icon {
    font-size: 3rem;
    color: var(--neon-red);
    margin-bottom: 16px;
}

.auth-lock-overlay h3 {
    font-size: 1.25rem;
    margin-bottom: 8px;
}

.auth-lock-overlay p {
    font-size: 0.85rem;
    color: var(--text-secondary);
    max-width: 400px;
    margin-bottom: 20px;
    line-height: 1.4;
}

.settings-group {
    margin-bottom: 28px;
}

.settings-group h3 {
    font-size: 1.05rem;
    margin-bottom: 12px;
    color: var(--text-secondary);
    border-left: 3px solid var(--neon-cyan);
    padding-left: 10px;
}

.mode-selector-radio {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
}

.radio-label {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: #ffffff;
    border: 1px solid var(--glass-border);
    padding: 16px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
}

.radio-label:hover {
    border-color: #cbd5e1;
    background: #f8fafc;
}

.radio-label input[type="radio"] {
    display: none;
}

.custom-radio {
    width: 18px;
    height: 18px;
    border: 2px solid var(--text-secondary);
    border-radius: 50%;
    display: inline-block;
    position: relative;
    flex-shrink: 0;
    margin-top: 2px;
}

.radio-label input[type="radio"]:checked + .custom-radio {
    border-color: var(--neon-cyan);
}

.radio-label input[type="radio"]:checked + .custom-radio::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--neon-cyan);
}

.radio-text strong {
    font-size: 0.9rem;
    margin-bottom: 2px;
    display: block;
}

.radio-text p {
    font-size: 0.75rem;
    color: var(--text-secondary);
    line-height: 1.3;
}

.sensor-config-rows {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.sensor-config-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    background: #ffffff;
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 16px 20px;
    gap: 16px;
}

.sensor-title {
    display: flex;
    align-items: center;
    gap: 16px;
}

.sensor-title i {
    font-size: 1.4rem;
    width: 28px;
    text-align: center;
}

.sensor-title strong {
    font-size: 0.9rem;
}

.sensor-title p {
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.sensor-inputs {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}

.input-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.input-field label {
    font-size: 0.72rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.input-field input {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    padding: 7px 12px;
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 0.85rem;
    width: 130px;
    outline: none;
    transition: border 0.2s;
}

.input-field input:focus {
    border-color: var(--neon-cyan);
}

.settings-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
}

/* About / Architecture page styles */
.subtitle-text {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: -12px;
    margin-bottom: 24px;
}

.architecture-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 28px;
    width: 100%;
}

.arch-col h3 {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--glass-border);
}

.arch-col ul {
    list-style: none;
}

.arch-col li {
    font-size: 0.84rem;
    color: var(--text-primary);
    line-height: 1.5;
    margin-bottom: 10px;
    position: relative;
    padding-left: 18px;
}

.arch-col li::before {
    content: '•';
    position: absolute;
    left: 4px;
    color: var(--neon-green);
    font-size: 1rem;
}

.formula-section {
    background: #f8fafc;
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 20px;
    margin-top: 24px;
}

.formula-section h3 {
    font-size: 1.1rem;
    margin-bottom: 8px;
}

.formula-intro {
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin-bottom: 16px;
}

.equation-box {
    background: #ffffff;
    border: 1px solid var(--glass-border);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    font-size: 1.25rem;
    color: var(--text-primary);
    margin-bottom: 20px;
}

.formula-variables {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    width: 100%;
}

.var-item strong {
    font-size: 0.85rem;
    color: var(--text-primary);
    display: block;
    margin-bottom: 4px;
}

.var-item p {
    font-size: 0.76rem;
    color: var(--text-secondary);
    line-height: 1.4;
}

/* Modals */
.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(15, 23, 42, 0.45);
    backdrop-filter: blur(6px);
    z-index: 1000;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 16px;
}

.modal {
    width: 100%;
    max-width: 420px;
    background: #ffffff;
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    animation: zoomIn 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes zoomIn {
    from { transform: scale(0.92); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: 12px;
    margin-bottom: 16px;
}

.modal-header h3 {
    font-size: 1.1rem;
}

.modal-close-btn {
    background: transparent;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 1.1rem;
}

.modal-close-btn:hover {
    color: var(--neon-red);
}

.form-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 16px;
}

.form-field label {
    font-size: 0.78rem;
    color: var(--text-secondary);
}

.form-field input {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    padding: 9px 12px;
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 0.85rem;
    outline: none;
    transition: all 0.2s;
}

.form-field input:focus {
    border-color: var(--neon-green);
    box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.alert {
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 0.8rem;
    margin-bottom: 15px;
    font-weight: 500;
}

.alert-danger {
    background: rgba(220, 38, 38, 0.1);
    color: var(--neon-red);
    border: 1px solid rgba(220, 38, 38, 0.2);
}

/* Helper Utilities */
.text-glow-green { color: var(--neon-green); }
.text-glow-amber { color: var(--neon-amber); }
.text-glow-cyan { color: var(--neon-cyan); }
.text-glow-violet { color: var(--neon-violet); }
.text-glow-red { color: var(--neon-red); }

.mr-1 { margin-right: 4px; }
.mr-2 { margin-right: 8px; }

/* Custom Slim Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

/* --- RESPONSIVE MEDIA QUERIES --- */
@media (max-width: 1100px) {
    .overview-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 1024px) {
    .sidebar {
        transform: translateX(-100%);
        z-index: 1000;
        width: 270px;
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.15);
    }
    .sidebar.open {
        transform: translateX(0);
    }
    .sidebar-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(4px);
        z-index: 999;
    }
    .sidebar-overlay.active {
        display: block;
    }
    .main-content {
        margin-left: 0;
        width: 100%;
        max-width: 100%;
        padding: 16px;
    }
    .mobile-nav-toggle {
        display: flex;
    }
}

@media (max-width: 900px) {
    .charts-section {
        grid-template-columns: 1fr;
    }
    .chart-container.full-width {
        grid-column: auto;
    }
}

@media (max-width: 600px) {
    .main-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }
    .header-controls {
        width: 100%;
        justify-content: flex-start;
    }
    .mode-status-container {
        width: 100%;
        justify-content: space-between;
    }
    .metrics-grid {
        grid-template-columns: 1fr;
    }
    .modal {
        width: 92vw;
    }
}
'''

# 3. New JS Content
APP_JS = r'''document.addEventListener("DOMContentLoaded", () => {
    // Current user state
    let currentUser = null;
    let autoUpdateInterval = null;
    
    // Chart references
    let chartEnergy = null;
    let chartWater = null;
    let chartClimate = null;

    // DOM Elements
    const tabTriggers = document.querySelectorAll(".sidebar-menu li");
    const tabPanels = document.querySelectorAll(".tab-panel");
    const btnExportPdf = document.getElementById("btn-export-pdf");
    const btnToggleFullscreen = document.getElementById("btn-toggle-fullscreen");
    const btnMobileToggle = document.getElementById("btn-mobile-toggle");
    const sidebar = document.querySelector(".sidebar");
    const sidebarOverlay = document.getElementById("sidebar-overlay");
    const currentTimeVal = document.getElementById("current-time-val");
    const loginTriggerBtn = document.getElementById("login-trigger-btn");
    const loginModal = document.getElementById("login-modal");
    const loginModalClose = document.getElementById("login-modal-close");
    const loginCancelBtn = document.getElementById("login-cancel-btn");
    const loginForm = document.getElementById("login-form");
    const loginErrorMsg = document.getElementById("login-error-msg");
    const profileName = document.getElementById("profile-name");
    const profileRole = document.getElementById("profile-role");
    
    // Circular Score SVGs
    const buildingScoreCircle = document.getElementById("building-score-circle");
    const valBuildingScore = document.getElementById("val-building-score");
    const valBuildingGrade = document.getElementById("val-building-grade");

    // Metric Displays
    const valEnergy = document.getElementById("val-energy");
    const scoreEnergy = document.getElementById("score-energy");
    const valWater = document.getElementById("val-water");
    const scoreWater = document.getElementById("score-water");
    const valTemp = document.getElementById("val-temp");
    const scoreClimate = document.getElementById("score-climate");
    const valCarbon = document.getElementById("val-carbon");
    const valHumidity = document.getElementById("val-humidity");
    const badgeAlertsCount = document.getElementById("badge-alerts-count");
    const activeAlertsTag = document.getElementById("active-alerts-tag");
    const modeIndicatorPill = document.getElementById("mode-indicator-pill");
    const modeText = document.getElementById("mode-text");

    // CSV elements
    const csvDropzone = document.getElementById("csv-dropzone");
    const csvFileInput = document.getElementById("csv-file-input");
    const csvFileName = document.getElementById("csv-file-name");
    const btnSubmitCsv = document.getElementById("btn-submit-csv");

    // Settings elements
    const settingsAuthOverlay = document.getElementById("settings-auth-overlay");
    const btnSettingsUnlock = document.getElementById("btn-settings-unlock");
    const btnSaveSettings = document.getElementById("btn-save-settings");

    // Set real-time clock
    function updateClock() {
        const now = new Date();
        currentTimeVal.textContent = now.toLocaleString();
    }
    setInterval(updateClock, 1000);
    updateClock();

    // --- FULLSCREEN TOGGLE SYSTEM ---
    if (btnToggleFullscreen) {
        btnToggleFullscreen.addEventListener("click", () => {
            if (!document.fullscreenElement) {
                if (document.documentElement.requestFullscreen) {
                    document.documentElement.requestFullscreen().catch(err => {
                        console.warn("Fullscreen request error:", err);
                    });
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
            }
        });

        document.addEventListener("fullscreenchange", () => {
            const icon = btnToggleFullscreen.querySelector("i");
            const span = btnToggleFullscreen.querySelector("span");
            if (document.fullscreenElement) {
                if (icon) icon.className = "fa-solid fa-compress";
                if (span) span.textContent = "Exit Fullscreen";
            } else {
                if (icon) icon.className = "fa-solid fa-expand";
                if (span) span.textContent = "Fullscreen";
            }
            setTimeout(resizeAllCharts, 200);
        });
    }

    // --- MOBILE SIDEBAR DRAWER SYSTEM ---
    if (btnMobileToggle && sidebar && sidebarOverlay) {
        btnMobileToggle.addEventListener("click", () => {
            sidebar.classList.toggle("open");
            sidebarOverlay.classList.toggle("active");
        });
        sidebarOverlay.addEventListener("click", () => {
            sidebar.classList.remove("open");
            sidebarOverlay.classList.remove("active");
        });
    }

    function resizeAllCharts() {
        if (chartEnergy) chartEnergy.resize();
        if (chartWater) chartWater.resize();
        if (chartClimate) chartClimate.resize();
    }
    window.addEventListener("resize", () => {
        resizeAllCharts();
    });

    // --- TAB NAVIGATION SYSTEM ---
    tabTriggers.forEach(trigger => {
        trigger.addEventListener("click", () => {
            const targetTab = trigger.getAttribute("data-tab");
            
            // Close mobile sidebar on tab selection
            if (window.innerWidth <= 1024 && sidebar && sidebarOverlay) {
                sidebar.classList.remove("open");
                sidebarOverlay.classList.remove("active");
            }

            // Update active menu item
            tabTriggers.forEach(t => t.classList.remove("active"));
            trigger.classList.add("active");

            // Update active content panel
            tabPanels.forEach(p => {
                p.classList.remove("active");
                if (p.getAttribute("id") === `tab-${targetTab}`) {
                    p.classList.add("active");
                }
            });

            // Adjust page title
            const titleMap = {
                dashboard: "Ecological Analytics",
                alerts: "Live System Alerts",
                upload: "CSV Audit Ingestion",
                leed: "LEED Design Certifier",
                logs: "Database Logs Explorer",
                settings: "Configuration Panels",
                about: "System Architecture"
            };
            document.getElementById("page-title").textContent = titleMap[targetTab] || "EcoBuild Dashboard";

            // If entering dashboard, refresh charts
            if (targetTab === "dashboard") {
                fetchStats();
                fetchCharts();
                setTimeout(resizeAllCharts, 150);
            } else if (targetTab === "alerts") {
                fetchAlerts();
            } else if (targetTab === "settings") {
                fetchSettings();
            } else if (targetTab === "logs") {
                fetchLogs();
            }
        });
    });

    // --- CHART.JS INITIALIZATION ---
    function initCharts() {
        const fontConfig = {
            family: "'Inter', sans-serif",
            size: 11,
            color: "#475569"
        };
        
        // 1. Energy Line Chart
        const ctxEnergy = document.getElementById("chart-energy").getContext("2d");
        chartEnergy = new Chart(ctxEnergy, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Power load (W)',
                    data: [],
                    borderColor: '#d97706',
                    backgroundColor: 'rgba(217, 119, 6, 0.06)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.35,
                    pointRadius: 3,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } },
                    y: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } }
                }
            }
        });

        // 2. Water Flow Chart
        const ctxWater = document.getElementById("chart-water").getContext("2d");
        chartWater = new Chart(ctxWater, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Flow rate (L/min)',
                    data: [],
                    borderColor: '#0891b2',
                    backgroundColor: 'rgba(8, 145, 178, 0.06)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.35,
                    pointRadius: 3,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } },
                    y: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } }
                }
            }
        });

        // 3. Thermal Comfort Double-Axis Line Chart
        const ctxClimate = document.getElementById("chart-climate").getContext("2d");
        chartClimate = new Chart(ctxClimate, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Temperature (°C)',
                        data: [],
                        borderColor: '#7c3aed',
                        backgroundColor: 'transparent',
                        borderWidth: 2.5,
                        tension: 0.35,
                        yAxisID: 'yTemp',
                        pointRadius: 3
                    },
                    {
                        label: 'Humidity (%)',
                        data: [],
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.04)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: true,
                        tension: 0.35,
                        yAxisID: 'yHumidity',
                        pointRadius: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: { color: '#475569', font: fontConfig, boxWidth: 12 }
                    }
                },
                scales: {
                    x: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { color: '#475569', font: fontConfig } },
                    yTemp: {
                        type: 'linear',
                        position: 'left',
                        grid: { color: 'rgba(0, 0, 0, 0.04)' },
                        ticks: { color: '#7c3aed', font: fontConfig }
                    },
                    yHumidity: {
                        type: 'linear',
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        ticks: { color: '#059669', font: fontConfig }
                    }
                }
            }
        });
    }

    // --- GAUGES AND SCORES UPDATE ---
    function setBuildingScore(score) {
        valBuildingScore.textContent = Math.round(score);
        const circumference = 2 * Math.PI * 70; // 439.82
        const offset = circumference - (score / 100) * circumference;
        buildingScoreCircle.style.strokeDashoffset = offset;

        // Set grade color and text
        if (score >= 80) {
            valBuildingGrade.textContent = "Platinum Rating (Exceptional)";
            valBuildingGrade.style.color = "var(--neon-green)";
            buildingScoreCircle.style.stroke = "var(--neon-green)";
        } else if (score >= 65) {
            valBuildingGrade.textContent = "Gold Rating (High Efficiency)";
            valBuildingGrade.style.color = "var(--neon-cyan)";
            buildingScoreCircle.style.stroke = "var(--neon-cyan)";
        } else if (score >= 50) {
            valBuildingGrade.textContent = "Silver Rating (Moderate)";
            valBuildingGrade.style.color = "var(--neon-amber)";
            buildingScoreCircle.style.stroke = "var(--neon-amber)";
        } else {
            valBuildingGrade.textContent = "Certified Baseline (Action Required)";
            valBuildingGrade.style.color = "var(--neon-red)";
            buildingScoreCircle.style.stroke = "var(--neon-red)";
        }
    }

    // --- DATA FETCHING & API INTERFACES ---
    async function fetchStats() {
        try {
            const res = await fetch('/api/stats');
            if (!res.ok) return;
            const data = await res.json();

            // Render Real-time metrics
            valEnergy.textContent = data.energy.value.toFixed(1);
            scoreEnergy.textContent = `${data.energy.score}/100`;

            valWater.textContent = data.water.value.toFixed(1);
            scoreWater.textContent = `${data.water.score}/100`;

            valTemp.textContent = data.climate.temp.toFixed(1);
            scoreClimate.textContent = `${data.climate.score}/100`;
            valHumidity.textContent = `${data.climate.humidity.toFixed(1)}%`;

            // Carbon emissions calculated: standard coefficient 0.82 kg CO2 / kWh
            const carbonKg = ((data.energy.value / 1000) * 0.82).toFixed(2);
            valCarbon.textContent = carbonKg;

            // Trees saved
            const treesEq = (carbonKg * 0.05).toFixed(1);
            const valTreesEl = document.getElementById("val-trees");
            if (valTreesEl) valTreesEl.textContent = treesEq;

            // Sustainability Goals Update
            const energyLimit = 3500;
            const energyPct = Math.min(100, Math.round((data.energy.value / energyLimit) * 100));
            const energyGoalProg = document.getElementById("energy-goal-progress");
            if (energyGoalProg) {
                energyGoalProg.style.width = `${energyPct}%`;
                energyGoalProg.style.background = energyPct > 90 ? 'var(--neon-red)' : (energyPct > 75 ? 'var(--neon-amber)' : 'var(--neon-green)');
            }
            const energyGoalCurr = document.getElementById("energy-goal-curr");
            if (energyGoalCurr) energyGoalCurr.textContent = `${data.energy.value.toFixed(0)} W`;
            const energyGoalPctEl = document.getElementById("energy-goal-pct");
            if (energyGoalPctEl) energyGoalPctEl.textContent = `${energyPct}% used`;

            const waterLimit = 25;
            const waterPct = Math.min(100, Math.round((data.water.value / waterLimit) * 100));
            const waterGoalProg = document.getElementById("water-goal-progress");
            if (waterGoalProg) {
                waterGoalProg.style.width = `${waterPct}%`;
                waterGoalProg.style.background = waterPct > 90 ? 'var(--neon-red)' : 'var(--neon-cyan)';
            }
            const waterGoalCurr = document.getElementById("water-goal-curr");
            if (waterGoalCurr) waterGoalCurr.textContent = `${data.water.value.toFixed(1)} L/m`;
            const waterGoalPctEl = document.getElementById("water-goal-pct");
            if (waterGoalPctEl) waterGoalPctEl.textContent = `${waterPct}% used`;

            // Overall Score
            setBuildingScore(data.building_score);

            // Anomaly Badge Count
            badgeAlertsCount.textContent = data.active_anomalies_count;
            if (data.active_anomalies_count > 0) {
                badgeAlertsCount.style.display = "inline-block";
            } else {
                badgeAlertsCount.style.display = "none";
            }
        } catch (err) {
            console.warn("Telemetry fetch stats error:", err);
        }
    }

    async function fetchCharts() {
        try {
            const res = await fetch('/api/charts');
            if (!res.ok) return;
            const data = await res.json();

            // Update Chart datasets
            if (chartEnergy) {
                chartEnergy.data.labels = data.energy.labels;
                chartEnergy.data.datasets[0].data = data.energy.values;
                chartEnergy.update();
            }

            if (chartWater) {
                chartWater.data.labels = data.water.labels;
                chartWater.data.datasets[0].data = data.water.values;
                chartWater.update();
            }

            if (chartClimate) {
                chartClimate.data.labels = data.climate.labels;
                chartClimate.data.datasets[0].data = data.climate.temp;
                chartClimate.data.datasets[1].data = data.climate.humidity;
                chartClimate.update();
            }
        } catch (err) {
            console.warn("Telemetry fetch charts error:", err);
        }
    }

    async function fetchAlerts() {
        try {
            const res = await fetch('/api/alerts');
            if (!res.ok) return;
            const data = await res.json();
            
            const tbody = document.getElementById("alerts-tbody");
            activeAlertsTag.textContent = `${data.length} Active Anomalies`;

            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" class="text-center">No anomalies registered. Systems functioning normally.</td></tr>`;
                return;
            }

            tbody.innerHTML = data.map(item => `
                <tr>
                    <td><span class="badge-outline-danger">${item.severity}</span></td>
                    <td><strong>${item.node_id}</strong></td>
                    <td>${item.value}</td>
                    <td>${item.threshold}</td>
                    <td>${item.timestamp}</td>
                    <td><span class="badge-outline-danger">Triggered</span></td>
                    <td>
                        <button class="action-link-btn" onclick="dismissAlert(${item.id})">Acknowledge</button>
                    </td>
                </tr>
            `).join("");
        } catch (err) {
            console.warn("Alerts fetch error:", err);
        }
    }

    window.dismissAlert = async function(id) {
        try {
            await fetch(`/api/alerts/${id}/dismiss`, { method: 'POST' });
            fetchAlerts();
            fetchStats();
        } catch (err) {
            console.error("Failed to dismiss alert:", err);
        }
    };

    async function fetchLogs() {
        try {
            const res = await fetch('/api/logs');
            if (!res.ok) return;
            const data = await res.json();
            
            const tbody = document.getElementById("logs-tbody");
            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="text-center">No persistent records found.</td></tr>`;
                return;
            }

            tbody.innerHTML = data.map(row => `
                <tr>
                    <td>#${row.id}</td>
                    <td><strong>${row.node_id}</strong></td>
                    <td>${row.value1 != null ? row.value1 : '-'}</td>
                    <td>${row.value2 != null ? row.value2 : '-'}</td>
                    <td><span class="badge-outline-success">${row.score != null ? row.score : '-'}</span></td>
                    <td>${row.timestamp}</td>
                </tr>
            `).join("");
        } catch (err) {
            console.warn("Logs fetch error:", err);
        }
    }

    const btnRefreshLogs = document.getElementById("btn-refresh-logs");
    if (btnRefreshLogs) {
        btnRefreshLogs.addEventListener("click", fetchLogs);
    }

    // --- LEED SCORING SYSTEM ---
    const leedCheckboxes = document.querySelectorAll(".leed-checkbox");
    const valLeedGrade = document.getElementById("val-leed-grade");

    function calculateLeedScore() {
        let total = 0;
        leedCheckboxes.forEach(cb => {
            if (cb.checked) total += parseInt(cb.value);
        });

        let grade = "Certified";
        if (total >= 80) grade = "LEED Platinum Rating";
        else if (total >= 60) grade = "LEED Gold Rating";
        else if (total >= 50) grade = "LEED Silver Rating";
        else if (total >= 40) grade = "LEED Certified Standard";
        else grade = "Targeting Certification";

        valLeedGrade.textContent = `${grade} (${total} Points)`;
    }

    leedCheckboxes.forEach(cb => {
        cb.addEventListener("change", calculateLeedScore);
    });

    // --- CSV UPLOAD INGESTION ---
    if (csvDropzone) {
        csvDropzone.addEventListener("click", () => csvFileInput.click());
        csvDropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            csvDropzone.classList.add("dragover");
        });
        csvDropzone.addEventListener("dragleave", () => csvDropzone.classList.remove("dragover"));
        csvDropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            csvDropzone.classList.remove("dragover");
            if (e.dataTransfer.files.length) {
                csvFileInput.files = e.dataTransfer.files;
                handleSelectedFile();
            }
        });

        csvFileInput.addEventListener("change", handleSelectedFile);
    }

    function handleSelectedFile() {
        if (csvFileInput.files.length > 0) {
            csvFileName.textContent = csvFileInput.files[0].name;
            csvDropzone.classList.add("has-file");
            btnSubmitCsv.removeAttribute("disabled");
        }
    }

    if (btnSubmitCsv) {
        btnSubmitCsv.addEventListener("click", async () => {
            if (!csvFileInput.files.length) return;
            const formData = new FormData();
            formData.append("file", csvFileInput.files[0]);

            btnSubmitCsv.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Ingesting dataset...`;
            btnSubmitCsv.setAttribute("disabled", "true");

            try {
                const res = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await res.json();
                alert(result.message || "CSV ingested successfully!");
                csvFileName.textContent = "No file selected";
                csvDropzone.classList.remove("has-file");
                csvFileInput.value = "";
                fetchStats();
            } catch (err) {
                alert("Failed to process CSV file.");
            } finally {
                btnSubmitCsv.innerHTML = `<i class="fa-solid fa-square-check"></i> <span>Start CSV Ingestion Process</span>`;
            }
        });
    }

    // --- AUTHENTICATION & LOGIN ---
    function openLoginModal() {
        loginModal.style.display = "flex";
    }

    function closeLoginModal() {
        loginModal.style.display = "none";
        loginErrorMsg.style.display = "none";
    }

    loginTriggerBtn.addEventListener("click", () => {
        if (currentUser) {
            // Logout
            currentUser = null;
            profileName.textContent = "Guest View";
            profileRole.textContent = "Limited Access";
            loginTriggerBtn.innerHTML = `<i class="fa-solid fa-right-to-bracket"></i>`;
            settingsAuthOverlay.style.display = "flex";
        } else {
            openLoginModal();
        }
    });

    loginModalClose.addEventListener("click", closeLoginModal);
    loginCancelBtn.addEventListener("click", closeLoginModal);

    btnSettingsUnlock.addEventListener("click", openLoginModal);

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const u = document.getElementById("login-username").value;
        const p = document.getElementById("login-password").value;

        try {
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: u, password: p })
            });
            const data = await res.json();

            if (res.ok && data.success) {
                currentUser = data.user;
                profileName.textContent = data.user.name;
                profileRole.textContent = data.user.role;
                loginTriggerBtn.innerHTML = `<i class="fa-solid fa-right-from-bracket" style="color: var(--neon-red);"></i>`;
                settingsAuthOverlay.style.display = "none";
                closeLoginModal();
                fetchSettings();
            } else {
                loginErrorMsg.style.display = "block";
            }
        } catch (err) {
            loginErrorMsg.style.display = "block";
        }
    });

    // --- SETTINGS FETCH & SAVE ---
    async function fetchSettings() {
        try {
            const res = await fetch('/api/settings');
            if (!res.ok) return;
            const data = await res.json();

            // Set system mode
            if (data.mode === 'live') {
                document.getElementById("mode-live").checked = true;
                modeIndicatorPill.classList.remove("demo-mode");
                modeText.textContent = "LIVE IoT MODE";
            } else {
                document.getElementById("mode-demo").checked = true;
                modeIndicatorPill.classList.add("demo-mode");
                modeText.textContent = "DEMO SIMULATION";
            }

            // Set Sensor Thresholds
            if (data.nodes) {
                if (data.nodes.node_energy) {
                    document.getElementById("input-thresh-energy").value = data.nodes.node_energy.threshold;
                    document.getElementById("input-cal-energy").value = data.nodes.node_energy.calibration_factor;
                }
                if (data.nodes.node_water) {
                    document.getElementById("input-thresh-water").value = data.nodes.node_water.threshold;
                    document.getElementById("input-cal-water").value = data.nodes.node_water.calibration_factor;
                }
                if (data.nodes.node_climate) {
                    document.getElementById("input-thresh-climate").value = data.nodes.node_climate.threshold;
                    document.getElementById("input-cal-climate").value = data.nodes.node_climate.calibration_factor;
                }
            }
        } catch (err) {
            console.warn("Failed to fetch settings:", err);
        }
    }

    if (btnSaveSettings) {
        btnSaveSettings.addEventListener("click", async () => {
            const selectedMode = document.querySelector('input[name="system-mode"]:checked').value;
            const settingsPayload = {
                mode: selectedMode,
                nodes: {
                    node_energy: {
                        threshold: parseFloat(document.getElementById("input-thresh-energy").value),
                        calibration_factor: parseFloat(document.getElementById("input-cal-energy").value)
                    },
                    node_water: {
                        threshold: parseFloat(document.getElementById("input-thresh-water").value),
                        calibration_factor: parseFloat(document.getElementById("input-cal-water").value)
                    },
                    node_climate: {
                        threshold: parseFloat(document.getElementById("input-thresh-climate").value),
                        calibration_factor: parseFloat(document.getElementById("input-cal-climate").value)
                    }
                }
            };

            try {
                const res = await fetch('/api/settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(settingsPayload)
                });
                if (res.ok) {
                    alert("System configuration and calibration saved successfully!");
                    fetchSettings();
                } else {
                    alert("Failed to save settings. Admin authentication required.");
                }
            } catch (err) {
                alert("Error connecting to server.");
            }
        });
    }

    // --- PDF EXPORT FEATURE ---
    if (btnExportPdf) {
        btnExportPdf.addEventListener("click", () => {
            const element = document.getElementById('printable-area');
            const opt = {
                margin: 0.3,
                filename: `EcoBuild_Report_${new Date().toISOString().slice(0,10)}.pdf`,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
            };
            html2pdf().set(opt).from(element).save();
        });
    }

    // --- INITIALIZE & START LOOP ---
    initCharts();
    fetchStats();
    fetchCharts();

    // Auto-refresh stats every 2.5 seconds
    autoUpdateInterval = setInterval(() => {
        fetchStats();
    }, 2500);

    // Auto-refresh charts every 5 seconds
    setInterval(() => {
        fetchCharts();
    }, 5000);
});'''

def main():
    print("Starting comprehensive dashboard update...")
    
    # 1. Update scratch frontend files
    scratch_frontend = os.path.join(SRC_DIR, "frontend")
    scratch_html = os.path.join(scratch_frontend, "index.html")
    scratch_css = os.path.join(scratch_frontend, "css", "style.css")
    scratch_js = os.path.join(scratch_frontend, "js", "app.js")

    os.makedirs(os.path.join(scratch_frontend, "css"), exist_ok=True)
    os.makedirs(os.path.join(scratch_frontend, "js"), exist_ok=True)

    with open(scratch_html, "w", encoding="utf-8") as f:
        f.write(INDEX_HTML)
    with open(scratch_css, "w", encoding="utf-8") as f:
        f.write(STYLE_CSS)
    with open(scratch_js, "w", encoding="utf-8") as f:
        f.write(APP_JS)
    print("Scratch frontend updated successfully.")

    # 2. Update scratch launcher
    scratch_launcher = os.path.join(SRC_DIR, "launcher", "start_dashboard.bat")
    bat_content = r'''@echo off
title Green Building Performance Dashboard Server
echo ==========================================================
echo    GREEN BUILDING PERFORMANCE DASHBOARD LAUNCHER
echo ==========================================================
echo.
echo Starting Flask web server in the background...

cd /d "%~dp0\..\backend"
start "EcoBuildServer" /B python app.py

echo Waiting for backend API to initialize (3 seconds)...
timeout /t 3 /nobreak > nul

echo Launching dashboard in maximized full-screen mode...
where chrome.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start "" "chrome.exe" --start-maximized --window-size=1920,1080 --app=http://127.0.0.1:5000
) else (
    where msedge.exe >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        start "" "msedge.exe" --start-maximized --window-size=1920,1080 --app=http://127.0.0.1:5000
    ) else (
        start http://127.0.0.1:5000
    )
)

echo.
echo ==========================================================
echo  Dashboard is active at http://127.0.0.1:5000
echo  Keep this console window open while using the app.
echo  Press any key in this window to stop the web server...
echo ==========================================================
echo.
pause

echo Stopping Flask web server...
taskkill /IM python.exe /F > nul 2>&1
echo Done!
timeout /t 2 > nul
'''
    with open(scratch_launcher, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print("Scratch launcher updated.")

    # 3. Update college_php_mysql_code
    college_dir = os.path.join(SRC_DIR, "college_php_mysql_code")
    college_css = os.path.join(college_dir, "style.css")
    college_js = os.path.join(college_dir, "app.js")
    if os.path.exists(college_dir):
        with open(college_css, "w", encoding="utf-8") as f:
            f.write(STYLE_CSS)
        with open(college_js, "w", encoding="utf-8") as f:
            f.write(APP_JS)
        print("College PHP/MySQL files updated.")

    # 4. Mirror everything into C:\Users\abc\green building dashboard
    if os.path.exists(DEST_DIR):
        for item in os.listdir(SRC_DIR):
            s = os.path.join(SRC_DIR, item)
            d = os.path.join(DEST_DIR, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        print(f"Synced completely to {DEST_DIR}")

    # 5. Re-run create_shortcut.ps1 to update desktop shortcut
    ps1_path = os.path.join(SRC_DIR, "launcher", "create_shortcut.ps1")
    if os.path.exists(ps1_path):
        try:
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1_path], check=True)
            print("Desktop shortcut updated successfully!")
        except Exception as e:
            print("Shortcut error:", e)

    print("ALL UPDATES COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
