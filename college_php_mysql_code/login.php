<?php
session_start();
header("Content-Type: application/json");
require_once("db_connect.php");

// Route 1: GET Session state
if ($_SERVER["REQUEST_METHOD"] === "GET") {
    if (isset($_SESSION["username"])) {
        echo json_encode(["logged_in" => true, "username" => $_SESSION["username"]]);
    } else {
        echo json_encode(["logged_in" => false]);
    }
    exit();
}

// Route 2: POST Login / Logout
$input = file_get_contents("php://input");
$data = json_decode($input, true);

$action = isset($data["action"]) ? $data["action"] : "login";

if ($action === "logout") {
    unset($_SESSION["username"]);
    session_destroy();
    echo json_encode(["success" => true, "message" => "Logged out"]);
    exit();
}

$username = isset($data["username"]) ? $data["username"] : "";
$password = isset($data["password"]) ? $data["password"] : "";

if (empty($username) || empty($password)) {
    http_response_code(400);
    echo json_encode(["success" => false, "message" => "Missing credentials"]);
    exit();
}

$pwd_hash = hash("sha256", $password);

$stmt = $conn->prepare("SELECT password_hash FROM users WHERE username = ?");
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();
$row = $result->fetch_assoc();
$stmt->close();

if ($row && $row["password_hash"] === $pwd_hash) {
    $_SESSION["username"] = $username;
    echo json_encode(["success" => true, "message" => "Login successful"]);
} else {
    http_response_code(401);
    echo json_encode(["success" => false, "message" => "Invalid username or password"]);
}

$conn->close();
?>
