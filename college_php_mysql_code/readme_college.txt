================================================================================
          GREEN BUILDING PERFORMANCE DASHBOARD - DEPLOYMENT GUIDE (XAMPP)
================================================================================

This folder contains the college-compliant source code built using PHP and MySQL.
To run this project on your local PC using XAMPP, follow these steps:

STEP 1: Start XAMPP Services
----------------------------
1. Open the XAMPP Control Panel.
2. Click the "Start" buttons next to Apache and MySQL. Ensure both modules show green lights.

STEP 2: Deploy Code Files
-------------------------
1. Copy this entire folder ("college_php_mysql_code") to your XAMPP installation directory:
   C:\xampp\htdocs\
2. Rename the pasted folder to "green_building_dashboard" for ease of access:
   C:\xampp\htdocs\green_building_dashboard

STEP 3: Initialize Database
---------------------------
1. Open your default web browser and navigate to: http://localhost/phpmyadmin
2. Click on the "Import" tab at the top.
3. Click "Choose File" and select the "database.sql" file located in:
   C:\xampp\htdocs\green_building_dashboard\database.sql
4. Scroll to the bottom of the page and click the "Go" or "Import" button.
   (This creates the `green_building_dashboard` database and populates baseline tables).

STEP 4: Access the Dashboard
----------------------------
1. Open your browser and navigate to:
   http://localhost/green_building_dashboard/
2. The interactive, modern dashboard will display.

STEP 5: Administrator Panel Login
---------------------------------
- Username: admin
- Password: admin123
- (This allows you to change alert thresholds and calibrate sensor variables).

================================================================================
                   PROJECT DOCUMENTATION JUSTIFICATION NOTES
================================================================================
This system implements:
1. Dual-Mode Acquisition: Renders live streams from ESP32 nodes via REST APIs OR legacy CSV spreadsheet uploads.
2. Building Efficiency Score (1-100): Calculated dynamically as:
   BES = 0.50 * Energy_Score + 0.30 * Water_Score + 0.20 * Climate_Score (ASHRAE 55)
3. Dynamic Graphs: Responsive Chart.js canvas renderings.
4. Active Alert Triggering: Automatic detection and cataloging of resource usage spikes.
5. Compliance PDF Auditor: Client-side PDF export system generating professional LEED documentation summaries.
================================================================================
