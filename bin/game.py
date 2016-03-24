from livewires import games, color
from player import *
from menuPointer import *
from surfaces import *
from exit import *
from hazard import *
from utilities import loadLevel

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
        for im in ['background']:
            image = games.load_image("Images\\" + im + ".bmp")
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

        logo = games.Text(value = "Aperture Science", size = 40, color = color.gray,
                                x = games.screen.width / 2 , y = 200)
        games.screen.add(logo)

        subHeader = "For science!"
        sub = games.Text(value = subHeader, size = 25, color = color.gray,
                                x = games.screen.width / 2 , y = 500)
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

    def Level(self, level, save):
        """
        Play the game
        """
        self.background(self.images[0])

        # Add info bar to top of screen
        self.infoBar()

        # Sprite containers
        self.portals = []
        self.surfaces = []
        self.neutrinos = []     # React with nothing

        self.orange = None
        self.blue = None

        surfaces, hazards, p, e = loadLevel(r"Levels\level1.json")

        for s in surfaces:
            box = Surface(game = self, x = s[0], y = s[1])
            games.screen.add(box)
            self.surfaces.append(box)

        for h in hazards:
            hazard = Hazard(game = self, x = h[0], y = h[1])
            games.screen.add(hazard)

        exit = Exit(game = self, x = e[0], y = e[1])
        games.screen.add(exit)

        player = Player(game = self, x = p[0], y = p[1])
        games.screen.add(player)
        self.player = player

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

    def endPlayerGame(self):
        """
        End the player controlled game
        """
        self.homescreen()

