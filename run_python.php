<?php
// Allow CORS
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, OPTIONS");

// Run the Python script
$output = shell_exec("python3 wardrobe.py > /dev/null 2>/dev/null &");
echo json_encode(["status" => "success", "message" => "Python script executed"]);
?>

