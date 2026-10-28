<?php
session_start();
header("Content-Type: application/json");
require_once("db_connect.php");

// 1. GET Settings Method
if ($_SERVER["REQUEST_METHOD"] === "GET") {
    // Get mode
    $res_mode = $conn->query("SELECT setting_value FROM settings WHERE setting_key = 'active_mode'");
    $mode_row = $res_mode->fetch_assoc();
    $mode = isset($mode_row["setting_value"]) ? $mode_row["setting_value"] : "LIVE";

    // Get sensors config
    $res_sensors = $conn->query("SELECT * FROM sensor_nodes");
    $sensors = [];
    while ($row = $res_sensors->fetch_assoc()) {
        $sensors[] = [
            "node_id" => $row["node_id"],
            "name" => $row["name"],
            "sensor_type" => $row["sensor_type"],
            "threshold" => floatval($row["threshold"]),
            "calibration_factor" => floatval($row["calibration_factor"])
        ];
    }

    echo json_encode([
        "mode" => $mode,
        "sensors" => $sensors
    ]);
    $conn->close();
    exit();
}

// 2. POST Update Settings Method
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Auth check
    if (!isset($_SESSION["username"])) {
        http_response_code(401);
        echo json_encode(["success" => false, "message" => "Unauthorized"]);
        exit();
    }

    $input = file_get_contents("php://input");
    $data = json_decode($input, true);

    $mode = isset($data["mode"]) ? $data["mode"] : null;
    $sensors = isset($data["sensors"]) ? $data["sensors"] : null;

    $conn->begin_transaction();

    if ($mode === "LIVE" || $mode === "DEMO") {
        $stmt_mode = $conn->prepare("UPDATE settings SET setting_value = ? WHERE setting_key = 'active_mode'");
        $stmt_mode->bind_param("s", $mode);
        $stmt_mode->execute();
        $stmt_mode->close();
    }

    if ($sensors && is_array($sensors)) {
        $stmt_sensor = $conn->prepare("UPDATE sensor_nodes SET name = COALESCE(?, name), threshold = COALESCE(?, threshold), calibration_factor = COALESCE(?, calibration_factor) WHERE node_id = ?");

        foreach ($sensors as $s) {
            $node_id = isset($s["node_id"]) ? $s["node_id"] : "";
            $name = isset($s["name"]) ? $s["name"] : null;
            $thresh = isset($s["threshold"]) ? floatval($s["threshold"]) : null;
            $cal = isset($s["calibration_factor"]) ? floatval($s["calibration_factor"]) : null;

            if (!empty($node_id)) {
                $stmt_sensor->bind_param("sdds", $name, $thresh, $cal, $node_id);
                $stmt_sensor->execute();
            }
        }
        $stmt_sensor->close();
    }

    $conn->commit();
    echo json_encode(["success" => true, "message" => "Settings updated successfully"]);
    $conn->close();
    exit();
}
?>
