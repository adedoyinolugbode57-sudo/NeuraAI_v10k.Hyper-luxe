import random

JOKES = [
    "Why don’t scientists trust mountains? They’re always up to something.",
    "Why did the plane get sent to its room? It had a bad altitude.",
    "Why did the passport break up with the plane? It felt carried away.",
    "Why did the luggage go to school? To get a little packing knowledge.",
    "Why did the beach break up with the tide? Too much wave action.",
    "Why did the travel agent quit? No one wanted to take the trip.",
    "Why did the compass go to therapy? Lost its direction.",
    "Why did the car go to school? To improve its mileage.",
    "Why did the suitcase blush? It saw the airport security.",
    "Why did the GPS break up? It couldn’t find the right direction.",
    "Why did the ship break up with the ocean? Too many waves.",
    "Why did the hotel go to therapy? Too many check-ins and check-outs.",
    "Why did the bicycle fall over? Too tired.",
    "Why did the map go to the party? To navigate social situations.",
    "Why did the bus bring a pillow? For a smooth ride."
]

def tell_joke() -> str:
    return random.choice(JOKES)