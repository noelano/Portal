from livewires import games, color
#from Player import *
#import os, random, string

games.init(screen_width = 1100, screen_height = 700, fps = 50)

# ============================================= #
# Class definitions for all objects in the game #

class Player(games.Sprite):
    """ The player controlled character """

    image1 = games.load_image("Images\\atlas1.bmp")
    image2 = games.load_image("Images\\atlas2.bmp")
    image3 = games.load_image("Images\\atlas5.bmp")
    image4 = games.load_image("Images\\atlas6.bmp")
    floor = 5 * games.screen.height / 7
    gravity = 0.02  # So jump looks more natural

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Player, self).__init__(image = Player.image1, x = x, y = y, dx = 0, dy = 0)
        self.game = game
        self.counter = 0    # To control the refresh of the sprite image

    def update(self):
        """ Move based on keys pressed. """
        self.counter += 1

        if self.y >= Player.floor and self.dy != 0:
            self.dy = 0
            self.y = Player.floor
        elif self.dy != 0:
            self.dy += Player.gravity

        if self.y == Player.floor and self.x > 10:
            if games.keyboard.is_pressed(games.K_LEFT):
                self.dx = -1
                if self.image in (Player.image1, Player.image2):
                    self.image = Player.image3
            if games.keyboard.is_pressed(games.K_RIGHT):
                self.dx = 1
                if self.image in (Player.image3, Player.image4):
                    self.image = Player.image1
            if games.keyboard.is_pressed(games.K_SPACE):
                self.dy = -2
            if not (games.keyboard.is_pressed(games.K_RIGHT) or games.keyboard.is_pressed(games.K_LEFT)):
                self.dx = 0

        # Stop player moving off screen to left
        if self.x < 40:
            self.x = 40
            self.dx = 0

        # Alternate between each image while moving to animate the sprite
        if self.dx > 0 and self.dy == 0:
            if self.counter % 30 == 0:
                self.image = Player.image2
            elif self.counter % 15 == 0:
                self.image = Player.image1
        elif self.dx < 0 and self.dy == 0:
            if self.counter % 30 == 0:
                self.image = Player.image3
            elif self.counter % 15 == 0:
                self.image = Player.image4

        self.checkCollisions()
        self.checkWin()

    def checkCollisions(self):
        """ Check if an obstacle is hit """

        if self.overlapping_sprites:
            end_message = games.Message(value = "Game Over. Learning...",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 1 * games.screen.fps,
                                    after_death = self.game.endPlayerGame)
            games.screen.add(end_message)

    def checkWin(self):
        """ See if the goal has been reached """

        if self.x > games.screen.width:
            end_message = games.Message(value = "Got it! Learning...",
                                    size = 90,
                                    color = color.blue,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 1 * games.screen.fps,
                                    after_death = self.game.endPlayerGame)
            games.screen.add(end_message)
			
class MenuPointer(games.Sprite):
    """
    Pointer for highlighting and making selections on the game menus
    """
    image = games.load_image("Images\\pointer.bmp")

    def __init__(self, game, x, y, menu):
        """ Initialize the sprite. """
        super(MenuPointer, self).__init__(image = MenuPointer.image, x = x, y = y, dx = 0, dy = 0)
        self.game = game
        self.selection = 0
        self.num_options = len(self.game.options) - 1
        self.menu = menu
        self.counter = 1

    def update(self):
        """
        Move the pointer up and down through the options list
        If the user hits enter proceed with the selected option
        """
        self.counter += 1

        # Because we have 50 fps a single button press could lead to a number
        # of updates ie one press of 'up' could scroll up 6 times.
        # To prevent this we add a buffer of 10 frames, which is what the counter
        # variable is used for

        if self.counter % 13 == 0:
            if self.num_options > 0:
                if games.keyboard.is_pressed(games.K_UP):
                    self.move(-1)
                if games.keyboard.is_pressed(games.K_DOWN):
                    self.move(1)
            if games.keyboard.is_pressed(games.K_RETURN):
                self.enter()

    def move(self, dir):
        """
        Move the pointer in the list based on the input direction 'dir'
        """
        old_selection = self.selection
        self.selection += dir

        # Check if we've gone beyond top of list and move to bottom
        # Likewise, go to the top if we move beyond the bottom
        if self.selection < 0:
            self.selection = self.num_options
        elif self.selection > self.num_options:
            self.selection = 0

        # Get y location of newly selected option
        option_location = self.game.options[self.selection].y

        # Put the pointer at this location
        self.y = option_location

        # Change option colours
        self.game.options[old_selection].color = color.white
        self.game.options[self.selection].color = color.blue

    def enter(self):
        """
        Perform an action based on the selected menu option
        """

        if self.menu == 0:
            if self.selection == 0:
                self.game.Level(1, 1, self.game.fileName)
            elif self.selection == 1:
                self.game.tutorial()
            else:
                games.screen.quit()

# ========================================= #
# Class for game screens and main functions #

class TeacherGame():
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

    def Level(self, level, playMode, save):
        """
        Play the game
        """
        self.background(self.images[0])

        # Add info bar to top of screen
        self.infoBar()

        # Add a list of sprites
        self.sprites = []

        player = Player(game = self,
                    x = games.screen.width/7,
                    y = 5*games.screen.height/7)
        games.screen.add(player)
        self.sprites.append(player)

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
        The computer will then learn from all the accumulated data
        """

        games.quit()

    def endCompGame(self):
        """
        End the player controlled game
        """
        games.music.stop()
        # Display top score. Add to save file
        self.levelMenu()

# ========================================== #
# End of class definitions - start the game! #

game = TeacherGame()
game.homescreen()
