// 🔥 Function to Save City Name to `city.txt` via PHP
function saveCityToFile(city) {
    fetch("save_city.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city: city })
    })
    .then(() => console.log("City saved successfully."))
    .catch(error => console.error("Error saving city:", error));
}

// 🔥 Function to Run `weather.py` via `run_weather.php`
function runWeatherPython() {
    fetch("run_weather.php") // Calls PHP script to execute `weather.py`
        .then(() => console.log("Weather script executed successfully."))
        .catch(error => console.error("Error running weather script:", error));
}

// 🔥 Function to Read Weather from `weather.txt` and Display It
function loadWeatherReport() {
    fetch("weather.txt?" + new Date().getTime()) // Prevents cache issues
        .then(response => response.text())
        .then(data => {
            const weatherReportElement = document.getElementById("weather-report");
            if (!weatherReportElement) {
                console.error("Error: #weather-report element not found.");
                return;
            }

            // 🔥 Display the weather inside a <pre> tag for proper formatting
            weatherReportElement.innerHTML = `<pre>${data}</pre>`;
        })
        .catch(error => {
            console.error("Error loading weather report:", error);
            document.getElementById("weather-report").innerHTML = "<p>Error fetching weather report.</p>";
        });
}

// 🔥 Event Listener for the City Input Form
document.getElementById("cityForm").addEventListener("submit", (event) => {
    event.preventDefault();  // 🔥 Prevents form from reloading the page

    const city = document.getElementById("cityInput").value.trim();
    if (city !== "") {
        saveCityToFile(city);  // 🔥 Save city to `city.txt`
        runWeatherPython();    // 🔥 Run Python script to update weather
        setTimeout(loadWeatherReport, 3000); // 🔄 Wait 3 seconds, then load weather
    } else {
        alert("Please enter a city name.");
    }
});

// 🔄 Refresh the Weather Report Every 10 Seconds
setInterval(loadWeatherReport, 10000);


