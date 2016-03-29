from livewires import games
from utilities import LOC

class SentryLOS(games.Sprite):
    """
    Object to allow the sentry to see
    """
    Lifetime = 50

    image = games.load_image(LOC + r"\..\Images\shot.bmp")

    def __init__(self, game, parent, x, y, dx):
        """ Initialize the sprite. """
        velocityFactor = 0.7

        super(SentryLOS, self).__init__(image = SentryLOS.image, x = x, y = y, dx = dx, dy = 0)
        self.game = game
        self.lifetime = SentryLOS.Lifetime
        self.parent = parent

    def update(self):
        """
        Move in a straight line until something is hit
        """

        # Destroy after set time
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()

        for sprite in self.overlapping_sprites:
            # Only interact with player or other sentries
            if sprite not in self.game.surfaces + self.game.neutrinos + self.game.cubes:
                self.parent.shootLaser()

            else:
                self.destroy()
