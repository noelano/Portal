from livewires import games, color
import math

class Reticule(games.Sprite):
    """
    Aiming reticule
    """

    image = games.load_image(r"Images\reticule.bmp")
    radius = 30
    rotation_step = 3

    def __init__(self, game, player, player_x, player_y):
        """ Initialize the sprite. """

        super(Reticule, self).__init__(image = Reticule.image, x = player_x + Reticule.radius, y = player_y, dx = 0, dy = 0)
        self.game = game
        self.baseX = player_x
        self.baseY = player_y
        self.theta = 0
        self.direction = 1
        self.player = player
        self.x_diff = 30
        self.y_diff = 0

    def update(self):
        """
        Angle the target, also handle firing a portal
        """
        self.baseX = self.player.x
        self.baseY = self.player.y

        self.y = self.baseY - self.y_diff

        if self.direction == 1:
            self.x = self.baseX + self.x_diff
        elif self.direction == 0:
            self.x = self.baseX - self.x_diff

        if games.keyboard.is_pressed(games.K_UP):
            if self.theta < 90:
                self.theta += Reticule.rotation_step
                self.x_diff = 30 * math.cos(self.theta * math.pi / 180)
                self.y_diff = 30 * math.sin(self.theta * math.pi / 180)

        if games.keyboard.is_pressed(games.K_DOWN):
            if self.theta > -90:
                self.theta -= Reticule.rotation_step
                self.x_diff = 30 * math.cos(self.theta * math.pi / 180)
                self.y_diff = 30 * math.sin(self.theta * math.pi / 180)

