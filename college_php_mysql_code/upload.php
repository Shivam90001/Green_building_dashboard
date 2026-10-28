<?php
header("Content-Type: application/json");
require_once("db_connect.php");

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["success" => false, "message" => "Method Not Allowed"]);
    exit();
}

if (!isset($_FILES["file"])) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "No file uploaded"]);
    exit();
}

$file = $_FILES["file"];
if ($file["error"] !== UPLOAD_ERR_OK) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "File upload error code: " . $file["error"]]);
    exit();
}

try {
    $content = file_get_contents($file["tmp_name"]);
    $lines = explode("\n", $content);

    // Set system mode to DEMO in settings
    $conn->query("UPDATE settings SET setting_value = 'DEMO' WHERE setting_key = 'active_mode'");

    $imported_count = 0;

    // Begin transaction for speed
    $conn->begin_transaction();

    $stmt_insert = $conn->prepare("INSERT INTO sensor_readings (node_id, value1, value2, mode, timestamp) VALUES (?, ?, ?, 'DEMO', ?)");

    // Loop through rows skipping header
    for ($i = 1; $i < count($lines); $i++) {
        $line = trim($lines[$i]);
        if (empty($line)) continue;

        $parts = explode(",", $line);
        if (count($parts) >= 2) {
            $node_id = trim($parts[0]);
            $val1 = floatval(trim($parts[1]));
            $val2 = (isset($parts[2]) && trim($parts[2]) !== "") ? floatval(trim($parts[2])) : null;
            $ts = (isset($parts[3]) && trim($parts[3]) !== "") ? trim($parts[3]) : date("Y-m-d H:i:s");

            // Check node exists
            $stmt_check = $conn->prepare("SELECT 1 FROM sensor_nodes WHERE node_id = ?");
            $stmt_check->bind_param("s", $node_id);
            $stmt_check->execute();
            $exists = $stmt_check->get_result()->fetch_assoc();
            $stmt_check->close();

            if ($exists) {
                $stmt_insert->bind_param("sdds", $node_id, $val1, $val2, $ts);
                $stmt_insert->execute();
                $imported_count++;
            }
        }
    }

    $stmt_insert->close();
    $conn->commit();

    echo json_encode([
        "success" => true,
        "message" => "Successfully imported $imported_count historical records. Switch to DEMO mode in Settings to visualize."
    ]);

} catch (Exception $e) {
    if (isset($conn)) $conn->rollback();
    http_response_code(500);
    echo json_encode(["success" => false, "message" => "Error parsing CSV: " . $e->getMessage()]);
}

$conn->close();
?>
