from livewires import games, color
import math

games.init(screen_width = 1100, screen_height = 700, fps = 50)

class PortalShot(games.Sprite):
    """
    Object to create portal
    """

    def __init__(self, game, x, y, angle):
        """ Initialize the sprite. """
        velocityFactor = 3
        dx = velocityFactor * math.sin(angle)
        dy = velocityFactor * -math.cos(angle)

        super(PortalShot, self).__init__(image = None, x = x, y = y, dx = dx, dy = dy)
        self.game = game
        self.angle = angle

    def update(self):
        """
        Move in a straight line until a surface is hit
        """

        # Destroy if we move off screen
        if (self.x < 0 or self.x > 1100 or y < 0 or y > 700):
            self.destroy()

        for sprite in self.overlapping_sprites:
            # Only interact with surface
            if sprite in self.game.surfaces:
                sprite.portal = 1
                self.destroy()
