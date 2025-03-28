import subprocess

def get_city():
    try:
        with open("city.txt", "r") as file:
            city = file.read().strip()
            return city if city else "Chandigarh"  # Default city if empty
    except FileNotFoundError:
        return "Chandigarh"  # Default city if no file exists

# 🔥 Function to Fetch Weather Using `curl wttr.in/CITY`
def get_weather(city):
    try:
        weather_data = subprocess.check_output(f"curl -s 'wttr.in/London?format=&2&n&T&d&F'", shell=True).decode("utf-8").strip()
        return weather_data
    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")
        return "Error fetching weather"

def main():
    city = get_city()
    weather = get_weather(city)

    with open("weather.txt", "w") as file:
        file.write(f"{weather}\n")  # 🔥 Save Weather & Outfit to `outfit.txt`
    print(f"Updated outfit recommendation for {city}.")

if __name__ == "__main__":
    main()

