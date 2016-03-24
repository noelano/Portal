from livewires import games, color
from player import *
from menuPointer import *
from surfaces import *
from exit import *
from hazard import *
from info import *
from textBox import *
from utilities import loadLevel, LOC
import os, pickle

class PortalGame():
    """
    Container class for the game
    """

    def __init__(self):
        """
        Define some game properties -
        Images and files that will be used later
        """
        self.fileName = None
        self.images = []
        self.level = None
        self.totalLevels = 1
        for im in ['title', 'background', 'credits']:
            image = games.load_image(LOC + "\..\\Images\\" + im + ".bmp")
            self.images.append(image)

    def background(self, image):
        """
        Prime the screen - clear any existing content and fill in the background
        """
        # cleanup any previous content
        games.screen.clear()

        # create background
        bck_image = image
        games.screen.background = bck_image

    def homescreen(self):
        """
        Game mainscreen
        """
        self.options = []
        self.background(self.images[0])

        subHeader = "For science!"
        sub = games.Text(value = subHeader, size = 25, color = color.gray,
                                x = games.screen.width / 2 , y = 600)
        games.screen.add(sub)

        menuOptions = ["Play Game", "Tutorial", "Quit"]
        for i in range(len(menuOptions)):
            label = games.Text(value = menuOptions[i], size = 25, color = color.white,
                                top = 300 + 30 * i , left = games.screen.width / 3)
            self.options.append(label)
            games.screen.add(label)

        # Set first option to blue
        self.options[0].color = color.blue

        pointer = MenuPointer(game = self,
                    x = games.screen.width/3 - 30,
                    y = 300,
                    menu = 0)
        games.screen.add(pointer)

        games.screen.mainloop()

    def loadGame(self):
        """
        Load a saved game
        """
        # Put the menu options in a list so the pointer can traverse them
        self.options = []

        # set background
        self.background(self.images[0])

        # Get the list of saved games from the save folder
        # Use os.listdir to get the names of all files in the folder
        files = [x.replace('.dat', '').upper() for x in os.listdir(LOC + r"\..\save") if '.dat' in x]

        while len(files) < 5:
            files.append('NEW GAME')

        for i in range(5):
            label = games.Text(value = files[i], size = 25, color = color.white,
                                top = 150 + 40 * i , left = games.screen.width / 3)
            self.options.append(label)
            games.screen.add(label)

        label = games.Text(value = "Back", size = 25, color = color.white,
                                top = 400 , left = games.screen.width / 3)
        self.options.append(label)
        games.screen.add(label)

        pointer = MenuPointer(game = self,
                    x = games.screen.width/3 - 30,
                    y = self.options[0].y,
                    menu = 1)
        games.screen.add(pointer)

    def levelMenu(self):
        """
        Menu to select which level will be played from those available
        """
        self.options = []
        self.background(self.images[0])

        # Load the saved records to find the highest level reached
        try:
            pickle_file = open(LOC + "\\..\\" + self.fileName, "rb")
            self.records = pickle.load(pickle_file)
            pickle_file.close()
            maxLevel = max(self.records.keys())
        except IOError:
            maxLevel = 0
            pickle_file = open(LOC + "\\..\\" + self.fileName, "wb")
            self.records = {1:None}
            pickle.dump(self.records, pickle_file)
            pickle_file.close()

        for i in range(maxLevel + 1):
            label = games.Text(value = 'Test ' + str(i + 1), size = 25, color = color.white,
                                top = 150 + 40 * i , left = games.screen.width / 3)
            self.options.append(label)
            games.screen.add(label)

        label = games.Text(value = "Back", size = 25, color = color.white,
                                top = 400 , left = games.screen.width / 3)
        self.options.append(label)
        games.screen.add(label)

        pointer = MenuPointer(game = self,
                    x = games.screen.width/3 - 30,
                    y = self.options[0].y,
                    menu = 2)
        games.screen.add(pointer)

        # Set first option to blue
        self.options[0].color = color.blue

    def Level(self, level, save):
        """
        Play the game
        """

        # Store the level for progression (Or failure)
        self.level = level
        self.background(self.images[1])

        # Add info bar to top of screen
        self.infoBar()

        # Sprite containers
        self.surfaces = []
        self.neutrinos = []     # React with nothing

        surfaces, hazards, p, e, start, end_message = loadLevel(LOC + "\\..\\Levels\\level" + str(level) + ".json")

        for s in surfaces:
            box = Surface(game = self, x = s[0], y = s[1])
            games.screen.add(box)
            self.surfaces.append(box)

        for h in hazards:
            hazard = Hazard(game = self, x = h[0], y = h[1])
            games.screen.add(hazard)

        exit = Exit(game = self, end_message = end_message, x = e[0], y = e[1])
        games.screen.add(exit)
        self.neutrinos.append(exit)

        player = Player(game = self, x = p[0], y = p[1])
        games.screen.add(player)
        self.player = player

        start_message = Info(message = start, size = 40, colour = color.light_gray, x = 550, y = 300, lifetime = 200)
        games.screen.add(start_message)
        self.neutrinos.append(start_message)

    def infoBar(self):
        """
        Display controls and game info across top of screen
        """
        message1 = "Move Left / Right: Arrow keys"
        label1 = games.Text(value = message1, size = 25, color = color.white,
                                top = 10 , left = 10)
        games.screen.add(label1)

        label2 = games.Text(value = "Jump: Spacebar", size = 25, color = color.white,
                                top = 40 , left = 10)
        games.screen.add(label2)

        label3 = games.Text(value = "Exit: Esc", size = 25, color = color.white,
                                top = 10 , left = 350)
        games.screen.add(label3)

        label4 = games.Text(value = "Return to menu: m", size = 25, color = color.white,
                                top = 40 , left = 350)
        games.screen.add(label4)

        self.score = games.Text(value = "Score: 0", size = 25, color = color.white,
                                top = 10 , left = 600)
        games.screen.add(self.score)

        self.time = games.Text(value = "Time: 0", size = 25, color = color.white,
                                top = 40 , left = 600)
        games.screen.add(self.time)

    def tutorial(self):
        """
        Info screen with background story and explanation of game mechanics
        """
        self.options = []
        self.background(self.images[0])

    def levelComplete(self):
        """
        End the player controlled game
        """
        self.records[self.level] = None
        pickle_file = open(LOC + "\\..\\" + self.fileName, "wb")
        pickle.dump(self.records, pickle_file)
        pickle_file.close()

        if self.level < self.totalLevels:
            self.level += 1
            self.Level(self.level, self.fileName)
        else:
            self.credits()

    def enterName(self):
        """
        Tent entry box to allow the user to enter a name
        """

        box = TextBox(game = self,
                    x = games.screen.width/2,
                    y = games.screen.height/2 + 40,)
        games.screen.add(box)

    def gameOver(self):
        self.levelMenu()

    def credits(self):
        self.background(self.images[2])
        message = Info("Game Over.", size = 40, colour = color.yellow, x = 550, y = -100, lifetime = 20000, dx = 0, dy = 0.3)
        games.screen.add(message)
