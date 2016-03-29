from livewires import games
from utilities import LOC

class Laser(games.Sprite):
    """
    Object to allow the sentry to see
    """
    Lifetime = 50

    image = games.load_image(LOC + r"\..\Images\laser.bmp")

    def __init__(self, game, x, y, dx):
        """ Initialize the sprite. """
        velocityFactor = 0.7

        super(Laser, self).__init__(image = Laser.image, x = x, y = y, dx = dx, dy = 0)
        self.game = game
        self.lifetime = Laser.Lifetime

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
            if sprite not in self.game.surfaces and sprite not in self.game.neutrinos:
                sprite.die()
                self.destroy()

            elif sprite in self.game.surfaces:
                self.destroy()
