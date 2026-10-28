<?php
header("Content-Type: application/json");
require_once("db_connect.php");

// 1. Fetch system mode
$res_mode = $conn->query("SELECT setting_value FROM settings WHERE setting_key = 'active_mode'");
$mode_row = $res_mode->fetch_assoc();
$mode = isset($mode_row["setting_value"]) ? $mode_row["setting_value"] : "LIVE";

// 2. Fetch sensor thresholds
$res_thresh = $conn->query("SELECT node_id, threshold FROM sensor_nodes");
$thresholds = [];
while ($row = $res_thresh->fetch_assoc()) {
    $thresholds[$row["node_id"]] = floatval($row["threshold"]);
}

$energy_thresh = isset($thresholds["node_energy"]) ? $thresholds["node_energy"] : 3500.0;
$water_thresh = isset($thresholds["node_water"]) ? $thresholds["node_water"] : 25.0;
$climate_thresh = isset($thresholds["node_climate"]) ? $thresholds["node_climate"] : 28.0;

// 3. Fetch latest readings for each node in current mode
$nodes = ["node_energy", "node_water", "node_climate"];
$latest_data = [];

foreach ($nodes as $node_id) {
    $stmt = $conn->prepare("SELECT value1, value2, timestamp FROM sensor_readings WHERE node_id = ? AND mode = ? ORDER BY timestamp DESC LIMIT 1");
    $stmt->bind_param("ss", $node_id, $mode);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();
    $stmt->close();

    if ($row) {
        $latest_data[$node_id] = [
            "val1" => floatval($row["value1"]),
            "val2" => ($row["value2"] !== null) ? floatval($row["value2"]) : null,
            "timestamp" => $row["timestamp"]
        ];
    } else {
        $latest_data[$node_id] = ["val1" => null, "val2" => null, "timestamp" => null];
    }
}

$energy_val = ($latest_data["node_energy"]["val1"] !== null) ? $latest_data["node_energy"]["val1"] : 0.0;
$water_val = ($latest_data["node_water"]["val1"] !== null) ? $latest_data["node_water"]["val1"] : 0.0;
$temp_val = ($latest_data["node_climate"]["val1"] !== null) ? $latest_data["node_climate"]["val1"] : 23.0;
$hum_val = ($latest_data["node_climate"]["val2"] !== null) ? $latest_data["node_climate"]["val2"] : 45.0;

// 4. Calculate scores
// Energy Score
$energy_pct = $energy_val / max(1.0, $energy_thresh);
if ($energy_pct <= 1.0) {
    $energy_score = 100.0 - ($energy_pct * 30.0);
} else {
    $energy_score = max(0.0, 70.0 - ($energy_pct - 1.0) * 100.0);
}

// Water Score
$water_pct = $water_val / max(1.0, $water_thresh);
if ($water_pct <= 1.0) {
    $water_score = 100.0 - ($water_pct * 30.0);
} else {
    $water_score = max(0.0, 70.0 - ($water_pct - 1.0) * 100.0);
}

// Climate Comfort Score (ASHRAE 55)
$temp_penalty = 0.0;
if ($temp_val < 20.0) {
    $temp_penalty = (20.0 - $temp_val) * 8.0;
} elseif ($temp_val > 25.0) {
    $temp_penalty = ($temp_val - 25.0) * 8.0;
}

$hum_penalty = 0.0;
if ($hum_val < 30.0) {
    $hum_penalty = (30.0 - $hum_val) * 1.2;
} elseif ($hum_val > 60.0) {
    $hum_penalty = ($hum_val - 60.0) * 1.2;
}
$climate_score = max(0.0, 100.0 - $temp_penalty - $hum_penalty);

// Final Weighted Building Efficiency Score
$weighted_score = (0.50 * $energy_score) + (0.30 * $water_score) + (0.20 * $climate_score);

// Carbon Footprint calculations
$energy_savings_w = max(0.0, $energy_thresh - $energy_val);
$carbon_saved_kg = round(($energy_savings_w / 1000.0) * 0.85, 2);

// Fetch unresolved alerts count
$res_alerts = $conn->query("SELECT COUNT(*) as count FROM alerts WHERE resolved = 0");
$alerts_row = $res_alerts->fetch_assoc();
$unresolved_alerts = isset($alerts_row["count"]) ? intval($alerts_row["count"]) : 0;

echo json_encode([
    "mode" => $mode,
    "latest_readings" => [
        "energy" => [
            "val" => round($energy_val, 1),
            "unit" => "W",
            "timestamp" => $latest_data["node_energy"]["timestamp"]
        ],
        "water" => [
            "val" => round($water_val, 1),
            "unit" => "L/min",
            "timestamp" => $latest_data["node_water"]["timestamp"]
        ],
        "climate" => [
            "temp" => round($temp_val, 1),
            "humidity" => round($hum_val, 1),
            "timestamp" => $latest_data["node_climate"]["timestamp"]
        ]
    ],
    "scores" => [
        "energy_score" => round($energy_score, 1),
        "water_score" => round($water_score, 1),
        "climate_score" => round($climate_score, 1),
        "building_score" => round($weighted_score, 1)
    ],
    "carbon_saved_kg" => $carbon_saved_kg,
    "unresolved_alerts" => $unresolved_alerts
]);

$conn->close();
?>
