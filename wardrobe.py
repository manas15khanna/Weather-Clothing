import requests
import time
import ollama
import random

# 🔥 Replace with your OpenWeatherMap API key
API_KEY = "db7f2850668839e7ccc717db791b3a00"

# 🔥 Wardrobe Data
WARDROBE = {
    "tops": ["White crewneck T-shirt", "Lime green crewneck T-shirt", "Dark grey crewneck T-shirt", "Maroon crewneck sweater", "Light grey crewneck sweater", "Dark grey polo", "Lilac Polo", "Green polo", "Black Oversized Polo", "White Polo with Stripes", "Black Polo", "Black Beach shirt", "Light grey GAP hoodie"],
    "bottoms": ["Black jeans", "Washed blue jeans", "Gray dark wash jeans",
                "Tan cargo pants", "Dark desert cargo pants", "White jeans"],
    "shoes": ["Adidas Samba sneakers", "New Balance 993", "Nike Dunk Low Black Grey Green Strike",
              "Adidas Ultraboost shoes", "Jordan 5 White Cement"],
    "accessories": ["Black Pearl Bracelet", "Black Ring", "Black Face watch", "White face watch", "Black Smartwatch"],
    "outer_layers": ["Light Gray Puffer Jacket", "Green Puffer Jacket"]
}


# 🔥 Function to Read City Name from File
def get_city():
    try:
        with open("city.txt", "r") as file:
            city = file.read().strip()
            return city if city else "Chandigarh"  # Default city if empty
    except FileNotFoundError:
        return "Chandigarh"  # Default city if no file exists

# 🔥 Function to Fetch Weather Data for the City
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url).json()
        if "main" in response:
            temp = response["main"]["temp"]
            conditions = response["weather"][0]["description"]
            return temp, conditions
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching weather for {city}: {e}")
        return None, None

# 🔥 Function to Generate Outfit Suggestion (AI-Powered)
def get_outfit_suggestion(temp, conditions):
    # 🔥 If it's cold (below 15°C), allow an outer layer
    outer_layer = ", ".join(WARDROBE["outer_layers"]) if temp < 15 else "None"

    # 🔥 AI Prompt (No Random Selection)
    prompt = f"""
    The weather in my city is {temp}°C with {conditions}. 
    Based on this, select an outfit from my wardrobe. 
    Only use the clothing items listed below:
    
    - Tops: {', '.join(WARDROBE["tops"])}
    - Bottoms: {', '.join(WARDROBE["bottoms"])}
    - Shoes: {', '.join(WARDROBE["shoes"])}
    - Accessories: {', '.join(WARDROBE["accessories"])}
    - Outer Layers (only if the weather is cold): {outer_layer}
    
    **IMPORTANT:**  
    - DO NOT create any new clothing items.  
    - DO NOT give long explanations.
    - DO NOT EXPLAIN 
    - DO NOT INCLUDE CODE
    - No astericks or any special characters
    - SELECT ONE ITEM FROM EACH CATEGORY
    """    
#    Format the response as: 
#    "Top: ..., Bottom: ..., Shoes: ..., Accessories: ...", and ONLY include an "Outer Layer" if it is cold.
    

    response = ollama.chat("qwen:0.5b", messages=[{"role": "user", "content": prompt}])

    if "message" in response and "content" in response["message"]:
        return response["message"]["content"]
    else:
        return "Could not generate an outfit recommendation."

# 🔥 Main Function to Continuously Update Outfit Recommendation
def main():
    #while True:
        city = get_city()  # 🔥 Read city from city.txt
        temp, conditions = get_weather(city)

        if temp is not None:
            outfit = get_outfit_suggestion(temp, conditions)

            # 🔥 Save Only Weather & Outfit to outfit.txt
            with open("outfit.txt", "w") as file:
                file.write(f"Weather in {city}: {temp}°C, {conditions}\n{outfit}")

            print(f"Updated outfit recommendation for {city}.")
        else:
            print(f"Could not fetch weather data for {city}.")

       # time.sleep(600)  # 🔄 Update every 10 minutes

if __name__ == "__main__":
    main()

