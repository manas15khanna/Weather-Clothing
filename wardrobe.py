import csv
import requests
import json
import os

# File Paths
CITY_FILE = "city.txt"
OUTPUT_FILE = "outfit.txt"
WARDROBE_FILE = "wardrobe.csv"

# Read city from city.txt
def read_city():
    if not os.path.exists(CITY_FILE):
        return None
    with open(CITY_FILE, "r", encoding="utf-8") as file:
        return file.read().strip()

# Fetch Full (QFn) and Summary (CtW) Weather from wttr.in
def get_weather(city):
    if not city:
        return "No city provided.", "Weather unavailable."

    full_weather_url = f"https://wttr.in/{city}?QTFn"  # Full weather report (QFn)
    summary_weather_url = f"https://wttr.in/{city}?format=%C+%t+%w"  # Short summary (CtW)

    try:
        full_weather = requests.get(full_weather_url).text.strip()
        summary_weather = requests.get(summary_weather_url).text.strip()
        return full_weather, summary_weather
    except Exception as e:
        return f"Error: {e}", "Weather unavailable."

# Load wardrobe from CSV
def load_wardrobe(csv_file):
    wardrobe = {}
    if not os.path.exists(csv_file):
        return {}

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                category, items = row[0], row[1:]
                wardrobe[category] = [item.strip() for item in items if item.strip()]
    return wardrobe

# Call Ollama Qwen locally to generate outfit
def get_qwen_outfit(wardrobe, weather_summary):
    import ollama  # Using local Ollama
    prompt = f"""Given this wardrobe: {json.dumps(wardrobe, indent=2)}
    and the weather: {weather_summary}, 
    select **one** item from each category to create a suitable outfit.
    Return only the final outfit, without explanations."""

    try:
        response = ollama.chat(model="qwen2.5:1.5b", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"] if "message" in response else "No response from Qwen."
    except Exception as e:
        return f"Error with Ollama: {e}"

# Save the full weather report and outfit to file
def save_outfit(full_weather, outfit, city):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(f"Weather Report for {city}:\n{full_weather}\n\n")
        file.write("Clothing Recommendation:\n")
        file.write(outfit)

# Main Execution
def main():
    city = read_city()
    if not city:
        print("Error: No city provided in city.txt")
        return

    # Get full weather (QFn) for display and short weather (CtW) for AI
    full_weather, weather_summary = get_weather(city)

    # Load wardrobe from CSV
    wardrobe = load_wardrobe(WARDROBE_FILE)

    # Get AI-generated outfit from Qwen
    outfit = get_qwen_outfit(wardrobe, weather_summary)

    # Save to outfit.txt
    save_outfit(full_weather, outfit, city)

    print("Outfit saved to outfit.txt")

# Run script
if __name__ == "__main__":
    main()

