// Function to Save City & Run Backend
function getWeatherAndOutfit(city) {
    fetch("run_wardrobe.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city: city })
    })
    .then(response => response.text())
    .then(() => {
        console.log("Weather & Outfit script executed.");
        setTimeout(loadReport, 3000);  // Wait for processing, then load results
    })
    .catch(error => console.error("Error:", error));
}

// Function to Load Weather & Outfit Report
function loadReport() {
    fetch("outfit.txt?" + new Date().getTime())  // Prevent cache issues
    .then(response => response.text())
    .then(data => {
        const sections = data.split("\n\n"); // Split weather and outfit
        document.getElementById("weather-report").innerText = sections[0] || "No data.";
        
        // Preserve line breaks for the outfit text
        const outfitBox = document.getElementById("outfit-report");
        outfitBox.innerHTML = sections[1] ? sections[1].replace(/\n/g, "<br>") : "No outfit suggestion.";
    })
    .catch(error => console.error("Error loading report:", error));
}

// Handle Form Submission
document.getElementById("cityForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const city = document.getElementById("cityInput").value.trim();
    if (city) getWeatherAndOutfit(city);
    else alert("Please enter a city.");
});

