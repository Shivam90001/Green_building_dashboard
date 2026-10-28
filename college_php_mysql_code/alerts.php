<?php
header("Content-Type: application/json");
require_once("db_connect.php");

// 1. GET alerts list
if ($_SERVER["REQUEST_METHOD"] === "GET") {
    $res = $conn->query("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 30");
    $alerts = [];
    while ($row = $res->fetch_assoc()) {
        $alerts[] = [
            "id" => intval($row["id"]),
            "node_id" => $row["node_id"],
            "reading_value" => floatval($row["reading_value"]),
            "threshold" => floatval($row["threshold"]),
            "message" => $row["message"],
            "timestamp" => $row["timestamp"],
            "resolved" => intval($row["resolved"]) === 1
        ];
    }
    echo json_encode($alerts);
    $conn->close();
    exit();
}

// 2. POST resolve alert
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $input = file_get_contents("php://input");
    $data = json_decode($input, true);

    $alert_id = isset($data["id"]) ? intval($data["id"]) : null;

    if (!$alert_id) {
        http_response_code(400);
        echo json_encode(["success" => false, "message" => "Missing alert id"]);
        exit();
    }

    $stmt = $conn->prepare("UPDATE alerts SET resolved = 1 WHERE id = ?");
    $stmt->bind_param("i", $alert_id);
    $stmt->execute();
    $stmt->close();

    echo json_encode(["success" => true, "message" => "Alert resolved successfully"]);
    $conn->close();
    exit();
}
?>
