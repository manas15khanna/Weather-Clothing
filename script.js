const cityElement = document.getElementById('city');
const temperatureElement = document.getElementById('temperature');
const conditionsElement = document.getElementById('conditions');
const iconElement = document.getElementById('icon');
const forecastElement = document.getElementById('forecast');
const weatherAdvice = document.getElementById('weather-advice');
const cityInput = document.getElementById('cityInput');
const getWeatherButton = document.getElementById('getWeatherButton');

// const apiKey = 'db7f2850668839e7ccc717db791b3a00'; // Replace with your OpenWeather API Key

getWeatherButton.addEventListener('click', () => {
    const city = cityInput.value.trim();
    if (city !== "") {
        saveCityToFile(city);
        getWeatherData(city);
        runWardrobePython();
    } else {
        alert("Please enter a city name.");
    }
});

function getWeatherData(city) {
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error("City not found");
            }
            return response.json();
        })
        .then(data => {
            cityElement.textContent = data.name;
            temperatureElement.textContent = `${data.main.temp}°C`;
            conditionsElement.textContent = data.weather[0].description;
            iconElement.src = `http://openweathermap.org/img/w/${data.weather[0].icon}.png`;

            const forecastApiUrl = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${apiKey}&units=metric`;
            return fetch(forecastApiUrl);
        })
        .then(response => response.json())
        .then(forecastData => {
            displayForecast(forecastData.list);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            cityElement.textContent = "Error: " + error.message;
        });
}

// 🔥 Function to send city name to PHP
function saveCityToFile(city) {
    fetch("save_city.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city: city })
    })
    .then(() => console.log("City saved successfully."))
    .catch(error => console.error("Error saving city:", error));
}

let usedTops = new Set();

// function displayForecast(forecastList) {
//     forecastElement.innerHTML = '';
//     weatherAdvice.innerHTML = '';
//
//     usedTops.clear();
//
//     for (let i = 0; i < 3; i++) {
//         const forecast = forecastList[i * 8];
//         if (!forecast) break;
//
//         const date = new Date(forecast.dt * 1000);
//         const day = date.toLocaleDateString('en-US', { weekday: 'long' });
//         const temp = forecast.main.temp;
//         const conditions = forecast.weather[0].description;
//         const iconCode = forecast.weather[0].icon;
//
//         const forecastDayDiv = document.createElement('div');
//         forecastDayDiv.classList.add('forecast-day');
//         forecastDayDiv.innerHTML = `
//             <img src="http://openweathermap.org/img/w/${iconCode}.png" alt="Forecast Icon">
//             <p>${day}: ${temp}°C - ${conditions}</p>
//         `;
//         forecastElement.appendChild(forecastDayDiv);
//
//         getOllamaClothingAdvice(temp, conditions, day);
//     }
// }
//
function getWeatherData(city) {
    const apiUrl = `https://wttr.in/${city}?0`;  // `?0` gives the full weather report without extras

    fetch(apiUrl)
        .then(response => response.text())
        .then(data => {
            // 🔥 Display the full ASCII weather report in a <pre> tag (preserves formatting)
            document.getElementById("weather-report").innerHTML = `<pre>${data}</pre>`;

            console.log(`Weather report fetched for ${city}`);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            document.getElementById("weather-report").innerHTML = "<p>Error fetching weather data.</p>";
        });
}

const userWardrobe = `Your JSON wardrobe data here`;

function runWardrobePython() {
    fetch("run_python.php") // Calls a PHP script that runs `wardrobe.py`
        .then(() => console.log("Python script executed successfully."))
        .catch(error => console.error("Error running Python script:", error));
}

async function getOllamaClothingAdvice() {
  fetch("outfit.txt?" + new Date().getTime()) // Prevents cache issues
        .then(response => response.text())
        .then(data => {
            if (!weatherAdvice) {
                console.error("Error: #weather-advice element not found.");
                return;
            }

            // 🔥 Split the outfit.txt data into weather and outfit details
            const lines = data.split("\n");
            const weatherInfo = lines[0] || "Weather data unavailable"; // Handle empty file case
            const outfitInfo = lines.slice(1).join("<br>") || "Outfit suggestion unavailable"; // Handle missing outfit case

            // 🔥 Update HTML elements safely
            weatherAdvice.innerHTML = `<h2>${weatherInfo}</h2><p>${outfitInfo}</p>`;
        })
        .catch(error => {
            console.error("Error loading outfit recommendation:", error);
            if (weatherAdvice) {
                weatherAdvice.innerHTML = "<p>Error fetching outfit recommendation.</p>";
            }
        });
}


setInterval(getOllamaClothingAdvice, 10000);

