# Miscellaneous functions
import math
import json

def distance(a, b):
    # Get distance between sprites a and b
    dist = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    return dist

def loadLevel(location):
    with open(location) as data_file:
        data = json.load(data_file)

    Surfaces = zip(data["Surface_x"], data["Surface_y"])
    Hazards = zip(data["Hazards_x"], data["Hazards_y"])
    Player = (data["Player_x"], data["Player_y"])
    Exit = (data["Exit_x"], data["Exit_y"])

    return Surfaces, Hazards, Player, Exit