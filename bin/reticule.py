from livewires import games
from portalSprite import *
import math
from utilities import LOC

class Reticule(games.Sprite):
    """
    Aiming reticule
    """

    image = games.load_image(LOC + r"\..\Images\reticule.bmp")
    radius = 35
    rotation_step = 2

    def __init__(self, game, player_x, player_y):
        """ Initialize the sprite. """

        super(Reticule, self).__init__(image = Reticule.image, x = player_x + Reticule.radius, y = player_y, dx = 0, dy = 0)
        self.game = game
        self.baseX = player_x
        self.baseY = player_y
        self.theta = 0
        self.direction = 1
        self.x_diff = 30
        self.y_diff = 0
        self.timer = 0

    def fireOrange(self):
        if self.timer == 0:
            dx = self.x - self.baseX
            dy = self.y - self.baseY
            orange = PortalShot(self.game, self.baseX, self.baseY, dx, dy, 0)
            games.screen.add(orange)
            self.timer = 60

    def fireBlue(self):
        if self.timer == 0:
            dx = self.x - self.baseX
            dy = self.y - self.baseY
            blue = PortalShot(self.game, self.baseX, self.baseY, dx, dy, 1)
            games.screen.add(blue)
            self.timer = 60

    def moveUp(self):
        if self.theta < 90:
            self.theta += Reticule.rotation_step
            self.x_diff = 30 * math.cos(self.theta * math.pi / 180)
            self.y_diff = 30 * math.sin(self.theta * math.pi / 180)

    def moveDown(self):
        if self.theta > -90:
            self.theta -= Reticule.rotation_step
            self.x_diff = 30 * math.cos(self.theta * math.pi / 180)
            self.y_diff = 30 * math.sin(self.theta * math.pi / 180)

    def movePosition(self, x, y):
        self.baseX = x
        self.baseY = y

        self.y = self.baseY - self.y_diff

        if self.direction == 1:
            self.x = self.baseX + self.x_diff
        elif self.direction == 0:
            self.x = self.baseX - self.x_diff

        # Timer delays portal shots
        if self.timer > 0:
            self.timer -= 1

