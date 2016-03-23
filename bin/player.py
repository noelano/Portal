from livewires import games, color
from portalSprite import *
from reticule import *

# Makes no sense having the init here but it works
# Must be required the first time a game object is initialised, which happens to be in the player???

class Player(games.Sprite):
    """ The player controlled character """

    image1 = games.load_image(r"Images\atlas1.bmp")
    image2 = games.load_image(r"Images\atlas2.bmp")
    image3 = games.load_image(r"Images\atlas5.bmp")
    image4 = games.load_image(r"Images\atlas6.bmp")
    floor = 5 * games.screen.height / 7
    gravity = 0.02  # So jump looks more natural

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Player, self).__init__(image = Player.image1, x = x, y = y, dx = 0, dy = 0)
        self.game = game
        self.counter = 0    # To control the refresh of the sprite image
        self.bottom = y + 31
        self.top = y - 31
        self.left = x - 21
        self.right = x + 21
        self.reticule = Reticule(self.game, self, self.x, self.y)
        games.screen.add(self.reticule)
        self.game.reticule.append(self.reticule)

    def update(self):
        """ Move based on keys pressed. """
        self.counter += 1

        if not self.overlapping_sprites:
            self.dy += Player.gravity

        if self.dy == 0:
            if games.keyboard.is_pressed(games.K_LEFT):
                self.dx = -1
                self.reticule.direction = 0
                if self.image in (Player.image1, Player.image2):
                    self.image = Player.image3
            if games.keyboard.is_pressed(games.K_RIGHT):
                self.dx = 1
                self.reticule.direction = 1
                if self.image in (Player.image3, Player.image4):
                    self.image = Player.image1
            if games.keyboard.is_pressed(games.K_SPACE):
                self.dy = -2
            if not (games.keyboard.is_pressed(games.K_RIGHT) or games.keyboard.is_pressed(games.K_LEFT)):
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

        self.checkWin()

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

    def firePortal(self):
        """
        Shoot a portal in the direction the user is facing
        """

        if games.keyboard.is_pressed(games.K_A):
            orangeHalo = PortalHalo()
            games.screen.add(orangeHalo)
            games.portals.add(orangeHalo)

        if games.keyboard.is_pressed(games.K_D):
            blueHalo = PortalHalo()
            games.screen.add(blueHalo)
            games.portals.add(blueHalo)

