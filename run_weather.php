<?php
// Allow CORS (for JavaScript fetch requests)
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, OPTIONS");

// Run the Python script to fetch weather
$output = shell_exec("python3 weather.py > /dev/null 2>/dev/null &");
echo json_encode(["status" => "success", "message" => "Weather script executed"]);
?>

