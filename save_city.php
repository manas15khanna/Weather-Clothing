<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER["REQUEST_METHOD"] === "OPTIONS") {
    http_response_code(200);
    exit();
}

$data = json_decode(file_get_contents("php://input"), true);
if (isset($data["city"])) {
    file_put_contents("city.txt", $data["city"]);
    echo json_encode(["success" => true]);
} else {
    echo json_encode(["error" => "City not provided"]);
}
?>

