<?php
header("Content-Type: application/json");
require_once("db_connect.php");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["success" => false, "message" => "Method Not Allowed"]);
    exit();
}

$input = file_get_contents("php://input");
$data = json_decode($input, true);

$node_id = isset($data["node_id"]) ? $data["node_id"] : null;
$value1 = isset($data["value1"]) ? floatval($data["value1"]) : null;
$value2 = isset($data["value2"]) ? floatval($data["value2"]) : null;

if (!$node_id || $value1 === null) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "Invalid payload parameters"]);
    exit();
}

// 1. Fetch sensor config (calibration_factor and threshold)
$stmt = $conn->prepare("SELECT calibration_factor, threshold, name FROM sensor_nodes WHERE node_id = ?");
$stmt->bind_param("s", $node_id);
$stmt->execute();
$result = $stmt->get_result();
$node = $result->fetch_assoc();

if (!$node) {
    http_response_code(404);
    echo json_encode(["success" => false, "message" => "Unknown sensor node"]);
    exit();
}
$stmt->close();

$calibrated_val1 = $value1 * $node["calibration_factor"];
$calibrated_val2 = ($value2 !== null) ? ($value2 * $node["calibration_factor"]) : null;

// 2. Fetch active mode from settings
$res_mode = $conn->query("SELECT setting_value FROM settings WHERE setting_key = 'active_mode'");
$mode_row = $res_mode->fetch_assoc();
$mode = isset($mode_row["setting_value"]) ? $mode_row["setting_value"] : "LIVE";

// 3. Save reading
$stmt_insert = $conn->prepare("INSERT INTO sensor_readings (node_id, value1, value2, mode, timestamp) VALUES (?, ?, ?, ?, NOW())");
$stmt_insert->bind_param("sddss", $node_id, $calibrated_val1, $calibrated_val2, $mode);
$stmt_insert->execute();
$stmt_insert->close();

// 4. Check thresholds and trigger alerts
$threshold = $node["threshold"];
$node_name = $node["name"];
$triggered = false;
$msg = "";

if ($node_id === 'node_energy' && $calibrated_val1 > $threshold) {
    $triggered = true;
    $msg = "Energy consumption spike: " . round($calibrated_val1, 1) . " W exceeded threshold of " . $threshold . " W on " . $node_name . ".";
} elseif ($node_id === 'node_water' && $calibrated_val1 > $threshold) {
    $triggered = true;
    $msg = "Water flow rate spike: " . round($calibrated_val1, 1) . " L/min exceeded threshold of " . $threshold . " L/min on " . $node_name . ".";
} elseif ($node_id === 'node_climate' && $calibrated_val1 > $threshold) {
    $triggered = true;
    $msg = "Temperature alert: " . round($calibrated_val1, 1) . "°C exceeded threshold of " . $threshold . "°C in Server Room.";
}

if ($triggered) {
    // Check for recent duplicate alert (last 5 minutes)
    $stmt_alert_check = $conn->prepare("SELECT id FROM alerts WHERE node_id = ? AND resolved = 0 AND timestamp > DATE_SUB(NOW(), INTERVAL 5 MINUTE)");
    $stmt_alert_check->bind_param("s", $node_id);
    $stmt_alert_check->execute();
    $alert_exists = $stmt_alert_check->get_result()->fetch_assoc();
    $stmt_alert_check->close();

    if (!$alert_exists) {
        $stmt_alert = $conn->prepare("INSERT INTO alerts (node_id, reading_value, threshold, message, timestamp, resolved) VALUES (?, ?, ?, ?, NOW(), 0)");
        $stmt_alert->bind_param("sdds", $node_id, $calibrated_val1, $threshold, $msg);
        $stmt_alert->execute();
        $stmt_alert->close();
    }
}

echo json_encode(["success" => true, "message" => "Data ingested successfully"]);
$conn->close();
?>
