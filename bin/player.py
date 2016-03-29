from livewires import games, color
from portalSprite import *
from reticule import *
from explosion import *
import math
from utilities import LOC, GRAVITY, TERMINAL_VELOCITY, AIR_RESISTANCE

# Makes no sense having the init here but it works
# Must be required the first time a game object is initialised, which happens to be in the player???

class Player(games.Sprite):
    """ The player controlled character """

    image1 = games.load_image(LOC + r"\..\Images\atlas1.bmp")
    image2 = games.load_image(LOC + r"\..\Images\atlas2.bmp")
    image3 = games.load_image(LOC + r"\..\Images\atlas5.bmp")
    image4 = games.load_image(LOC + r"\..\Images\atlas6.bmp")

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Player, self).__init__(image = Player.image1, x = x, y = y, dx = 0, dy = 0)
        self.game = game
        self.counter = 0    # To control the refresh of the sprite image
        self.reticule = Reticule(self.game, self.x, self.y)
        games.screen.add(self.reticule)
        self.game.neutrinos.append(self.reticule)
        self.speed = 0

    def update(self):
        """ Move based on keys pressed. """
        self.counter += 1
        self.calcSpeed()

        if (not self.overlapping_sprites or set(self.overlapping_sprites).issubset(self.game.neutrinos)) \
                and self.dy < TERMINAL_VELOCITY:
            self.dy += GRAVITY
            self.dx *= AIR_RESISTANCE

        if games.keyboard.is_pressed(games.K_LEFT):
            if self.dy == 0:
                self.dx = -1
            self.reticule.direction = 0
            if self.image in (Player.image1, Player.image2):
                self.image = Player.image3
        if games.keyboard.is_pressed(games.K_RIGHT):
            if self.dy == 0:
                self.dx = 1
            self.reticule.direction = 1
            if self.image in (Player.image3, Player.image4):
                self.image = Player.image1
        if self.dy == 0 and games.keyboard.is_pressed(games.K_SPACE):
            self.dy = -2
        if self.dy == 0 and not (games.keyboard.is_pressed(games.K_RIGHT) or games.keyboard.is_pressed(games.K_LEFT)):
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

        # This section controls the reticule actions, including firing, aiming and shooting
        # Shoot portals:
        if games.keyboard.is_pressed(games.K_a):
            self.reticule.fireOrange()
        if games.keyboard.is_pressed(games.K_d):
            self.reticule.fireBlue()

        # Change aim
        if games.keyboard.is_pressed(games.K_UP) and not games.keyboard.is_pressed(games.K_SPACE):
            self.reticule.moveUp()
        if games.keyboard.is_pressed(games.K_DOWN) and not games.keyboard.is_pressed(games.K_SPACE):
            self.reticule.moveDown()

        # Track player position
        self.reticule.movePosition(self.x, self.y)

    def checkWin(self):
        """ See if the goal has been reached """

        if self.x > games.screen.width:
            end_message = games.Message(value = "Congratulations",
                                    size = 90,
                                    color = color.blue,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 1 * games.screen.fps,
                                    after_death = self.game.endPlayerGame)
            games.screen.add(end_message)

    def calcSpeed(self):
        self.speed = math.sqrt(self.dx**2 + self.dy**2)

    def die(self):
        new_explosion = Explosion(x = self.x, y = self.y)
        games.screen.add(new_explosion)
        self.destroy()
        self.reticule.destroy()
        #self.game.gameOver()