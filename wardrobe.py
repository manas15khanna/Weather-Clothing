import subprocess
import ollama

# 🔥 Function to Load Clothing Data from `clothes.txt`
def load_wardrobe():
    wardrobe = {}
    try:
        with open("clothes.txt", "r") as file:
            for line in file:
                if ":" in line:
                    category, items = line.strip().split(":", 1)
                    wardrobe[category.strip()] = [item.strip() for item in items.split(",")]
    except FileNotFoundError:
        print("Error: clothes.txt not found. Using an empty wardrobe.")
    return wardrobe

# 🔥 Function to Read City Name from File
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
        weather_data = subprocess.check_output(f"curl -s 'wttr.in/{city}?format=%C+%t+%w+%h+%p'", shell=True).decode("utf-8").strip()
        return weather_data
    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")
        return "Error fetching weather"

# 🔥 Function to Generate Outfit Suggestion (AI-Powered)
def get_outfit_suggestion(wardrobe, weather_data):
    outer_layer = ", ".join(wardrobe["outer_layers"])

    prompt = f"""
    The WEATHER IS {weather_data}.
    Based on this, select an outfit from my wardrobe. 
    Only use the clothing items listed below:
    
    - Tops: {', '.join(wardrobe["tops"])}
    - Bottoms: {', '.join(wardrobe["bottoms"])}
    - Shoes: {', '.join(wardrobe["shoes"])}
    - Accessories: {', '.join(wardrobe["accessories"])}
    - Outer Layers (only if the weather is cold): {outer_layer}

    **IMPORTANT:**  
    - DO NOT create any new clothing items.  
    - DO NOT give long explanations.
    - DO NOT EXPLAIN 
    - DO NOT INCLUDE CODE
    - No asterisks or any special characters
    """    

    response = ollama.chat("qwen:1.8b", messages=[{"role": "user", "content": prompt}])

    if "message" in response and "content" in response["message"]:
        return response["message"]["content"]
    else:
        return "Could not generate an outfit recommendation."

# 🔥 Main Function to Continuously Update Outfit Recommendation
def main():
    wardrobe = load_wardrobe()  # Load wardrobe from file
    city = get_city()
    weather = get_weather(city)

    with open("outfit.txt", "w") as file:
        file.write(f"Weather in {city}: {weather}\n")  # 🔥 Save Weather & Outfit to `outfit.txt`

    print(f"Updated outfit recommendation for {city}.")

if __name__ == "__main__":
    main()

