# Miscellaneous functions
import math
import json
import os

# Define constants
LOC = os.getcwd()
if 'bin' not in LOC:
    LOC += '\\bin'
GRAVITY = 0.035
TERMINAL_VELOCITY = 2.8
AIR_RESISTANCE = 0.999


def distance(a, b):
    # Get distance between sprites a and b
    dist = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    return dist


def loadLevel(location):
    # Level details are stored in json files
    with open(location) as data_file:
        data = json.load(data_file)

    Surfaces = zip(data["Surface_x"], data["Surface_y"])
    Hazards = zip(data["Hazards_x"], data["Hazards_y"])
    Player = (data["Player_x"], data["Player_y"])
    Exit = (data["Exit_x"], data["Exit_y"])
    Bad_Surfaces = zip(data["Bad_Surface_x"], data["Bad_Surface_y"])
    Enemies = zip(data["Enemies_x"], data["Enemies_y"])
    Switch = (data["Switch_x"], data["Switch_y"])
    Dispenser = (data["Dispenser_x"], data["Dispenser_y"])
    Button = (data["Button_x"], data["Button_y"])

    return Surfaces, Bad_Surfaces, Hazards, Enemies, Player, Exit, Switch, data["Start"], data["End"], Dispenser, Button
