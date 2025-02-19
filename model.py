import ollama
import random
from wardrobe import wardrobe

def get_outfit_suggestion(temp, conditions, used_tops):
    top = random.choice([t for t in wardrobe["tops"] if t not in used_tops])
    bottom = random.choice(wardrobe["bottoms"])
    shoes = random.choice(wardrobe["shoes"])
    accessories = random.choice(wardrobe["accessories"])
    
    prompt = f"""
    The weather is {temp}°C with {conditions}. Suggest an outfit using the following wardrobe categories:
    - Top: {top}
    - Bottom: {bottom}
    - Shoes: {shoes}
    - Accessories: {accessories}
    Ensure the outfit is weather-appropriate.
    """
    
    response = ollama.chat("smollm", messages=[
        {"role": "system", "content": "You are a fashion assistant providing outfit recommendations based on weather conditions."},
        {"role": "user", "content": prompt}
    ])
    
    used_tops.add(top)
    return response["message"]["content"]

# Example usage
temp = 20  # Example temperature
conditions = "Partly Cloudy"  # Example condition
used_tops = set()  # Track used tops
outfit = get_outfit_suggestion(temp, conditions, used_tops)
print("Suggested Outfit:", outfit)

