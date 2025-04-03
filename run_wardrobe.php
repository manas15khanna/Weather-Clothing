<?php
$data = json_decode(file_get_contents("php://input"), true);
if (isset($data["city"])) {
    file_put_contents("city.txt", $data["city"]); // Save city
    exec("python3 wardrobe.py"); // Run Python script
    echo "Processing..."; // Send response
} else {
    echo "City not received.";
}
?>

