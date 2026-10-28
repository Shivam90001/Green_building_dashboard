<?php
header("Content-Type: application/json");
require_once("db_connect.php");

// 1. Fetch system mode
$res_mode = $conn->query("SELECT setting_value FROM settings WHERE setting_key = 'active_mode'");
$mode_row = $res_mode->fetch_assoc();
$mode = isset($mode_row["setting_value"]) ? $mode_row["setting_value"] : "LIVE";

// 2. Fetch last 20 energy records
$stmt_energy = $conn->prepare("SELECT timestamp, value1 FROM sensor_readings WHERE node_id = 'node_energy' AND mode = ? ORDER BY timestamp DESC LIMIT 20");
$stmt_energy->bind_param("s", $mode);
$stmt_energy->execute();
$res_energy = $stmt_energy->get_result();
$energy_rows = [];
while ($row = $res_energy->fetch_assoc()) {
    $energy_rows[] = $row;
}
$stmt_energy->close();
$energy_rows = array_reverse($energy_rows);

// Fetch last 20 water records
$stmt_water = $conn->prepare("SELECT timestamp, value1 FROM sensor_readings WHERE node_id = 'node_water' AND mode = ? ORDER BY timestamp DESC LIMIT 20");
$stmt_water->bind_param("s", $mode);
$stmt_water->execute();
$res_water = $stmt_water->get_result();
$water_rows = [];
while ($row = $res_water->fetch_assoc()) {
    $water_rows[] = $row;
}
$stmt_water->close();
$water_rows = array_reverse($water_rows);

// Fetch last 20 climate records
$stmt_climate = $conn->prepare("SELECT timestamp, value1, value2 FROM sensor_readings WHERE node_id = 'node_climate' AND mode = ? ORDER BY timestamp DESC LIMIT 20");
$stmt_climate->bind_param("s", $mode);
$stmt_climate->execute();
$res_climate = $stmt_climate->get_result();
$climate_rows = [];
while ($row = $res_climate->fetch_assoc()) {
    $climate_rows[] = $row;
}
$stmt_climate->close();
$climate_rows = array_reverse($climate_rows);

// Align timestamps. Combine and sort all timestamps
$timestamps = [];
foreach ($energy_rows as $r) { $timestamps[] = $r["timestamp"]; }
foreach ($water_rows as $r) { $timestamps[] = $r["timestamp"]; }
foreach ($climate_rows as $r) { $timestamps[] = $r["timestamp"]; }

$timestamps = array_unique($timestamps);
sort($timestamps);

// Slice to last 20
$timestamps = array_slice($timestamps, -20);

// Maps for values
$energy_map = [];
foreach ($energy_rows as $r) { $energy_map[$r["timestamp"]] = floatval($r["value1"]); }

$water_map = [];
foreach ($water_rows as $r) { $water_map[$r["timestamp"]] = floatval($r["value1"]); }

$temp_map = [];
$hum_map = [];
foreach ($climate_rows as $r) {
    $temp_map[$r["timestamp"]] = floatval($r["value1"]);
    $hum_map[$r["timestamp"]] = floatval($r["value2"]);
}

// Build output structure
$chart_data = [
    "labels" => [],
    "energy" => [],
    "water" => [],
    "temp" => [],
    "humidity" => []
];

foreach ($timestamps as $ts) {
    // Format timestamp as time string for labels
    $formatted_time = $ts;
    $dt = date_create($ts);
    if ($dt) {
        $formatted_time = date_format($dt, "H:i:s");
    }

    $chart_data["labels"][] = $formatted_time;
    $chart_data["energy"][] = isset($energy_map[$ts]) ? round($energy_map[$ts], 1) : 0.0;
    $chart_data["water"][] = isset($water_map[$ts]) ? round($water_map[$ts], 1) : 0.0;
    $chart_data["temp"][] = isset($temp_map[$ts]) ? round($temp_map[$ts], 1) : 23.0;
    $chart_data["humidity"][] = isset($hum_map[$ts]) ? round($hum_map[$ts], 1) : 45.0;
}

echo json_encode($chart_data);
$conn->close();
?>
