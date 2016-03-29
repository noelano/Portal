from livewires import games, color
from player import *
from menuPointer import *
from surfaces import *
from exit import *
from hazard import *
from info import *
from textBox import *
from badSurface import *
from sentry import *
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
        self.totalLevels = 11
        for im in ['Title', 'background', 'credits', 'Tutorial']:
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

    def tutorial(self):
        """
        Info screen with explanation of game mechanics
        """
        self.options = []
        self.background(self.images[3])

        label = games.Text(value = "Back", size = 25, color = color.blue,
                                top = 650 , left = games.screen.width / 2)
        self.options.append(label)
        games.screen.add(label)

        pointer = MenuPointer(game = self,
                    x = games.screen.width/2 - 30,
                    y = label.y,
                    menu = 1)
        games.screen.add(pointer)

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

        pointer = MenuPointer(game=self,
                    x=games.screen.width/3 - 30,
                    y=self.options[0].y,
                    menu=1)
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
            if i > 11:
                x_pos = 2 * games.screen.width / 3 + 15
            elif i > 5:
                x_pos = games.screen.width / 2 - 15
            else:
                x_pos = games.screen.width / 3 - 15
            label = games.Text(value='Test ' + str(i + 1), size=25, color=color.white,
                                top=150 + 40 * (i % 6), left=x_pos)
            self.options.append(label)
            games.screen.add(label)

        label = games.Text(value="Back", size=25, color=color.white,
                                top=400, left=games.screen.width / 3)
        self.options.append(label)
        games.screen.add(label)

        pointer = MenuPointer(game=self,
                    x=games.screen.width/3 - 30,
                    y=self.options[0].y,
                    menu=2)
        games.screen.add(pointer)

        # Set first option to blue
        self.options[0].color = color.blue

    def Level(self, level, save):
        """
        Play the game
        """
        # Make sure no portals are left hanging around
        Surface.orangePortal = None
        Surface.bluePortal = None

        # Store the level for progression (Or failure)
        self.level = level
        self.background(self.images[1])

        # Sprite containers
        self.surfaces = []
        self.neutrinos = []     # React with nothing

        layout = loadLevel(LOC + "\\..\\Levels\\level" + str(level) + ".json")

        for s in layout[0]:
            box = Surface(game=self, x=s[0], y=s[1])
            games.screen.add(box)
            self.surfaces.append(box)

        for b in layout[1]:
            bad = BadSurface(game=self, x=b[0], y=b[1])
            games.screen.add(bad)
            self.surfaces.append(bad)

        for h in layout[2]:
            hazard = Hazard(game=self, x=h[0], y=h[1])
            games.screen.add(hazard)

        if layout[6][0]:
            exit = Exit(game=self,
                        end_message=layout[8],
                        x=layout[5][0],
                        y=layout[5][1],
                        has_button=1,
                        button_x=layout[6][0],
                        button_y=layout[6][1])
        else:
            exit = Exit(game=self, end_message=layout[8], x=layout[5][0], y=layout[5][1])
        games.screen.add(exit)
        self.neutrinos.append(exit)

        for e in layout[3]:
            enemy = Sentry(game=self, x=e[0], y=e[1])
            games.screen.add(enemy)

        # Determine which faces are exposed on each surface
        # Portals can only be placed on these sides
        for sprite in self.surfaces:
            if type(sprite) == Surface:
                sprite.calculateExposedFaces()

        player = Player(game=self, x=layout[4][0], y=layout[4][1])
        games.screen.add(player)
        self.player = player

        start_message = Info(message=layout[7], size=30, colour=color.white, x=550, y=300, lifetime=200)
        games.screen.add(start_message)
        self.neutrinos.append(start_message)

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
        message = Info("Thank you for participating.",
                       size = 40,
                       colour = color.yellow,
                       x = 550,
                       y = -100,
                       lifetime = 20000,
                       dx = 0,
                       dy = 0.3)
        games.screen.add(message)
