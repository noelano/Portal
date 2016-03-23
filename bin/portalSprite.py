from livewires import games, color
import math

games.init(screen_width = 1100, screen_height = 700, fps = 50)

class PortalShot(games.Sprite):
    """
    Object to create portal
    """

    image = games.load_image(r"Images\shot.bmp")

    def __init__(self, game, x, y, dx, dy, colour):
        """ Initialize the sprite. """
        velocityFactor = 1

        super(PortalShot, self).__init__(image = PortalShot.image, x = x, y = y, dx = velocityFactor * dx, dy = velocityFactor * dy)
        self.game = game
        self.lifetime = 30
        self.colour = colour

    def update(self):
        """
        Move in a straight line until a surface is hit
        """

        # Destroy after set time
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()

        for sprite in self.overlapping_sprites:
            # Only interact with surface
            if sprite in self.game.surfaces:
                orientation = 0
                if self.x > sprite.x:
                    if self.y > sprite.y and (self.y - sprite.y < self.x - sprite.x):
                        orientation = 2
                    elif self.y > sprite.y:
                        orientation = 3
                    else:
                        orientation = 0
                else:
                    if self.y > sprite.y and (self.y - sprite.y < sprite.x - self.x):
                        orientation = 1
                    elif self.y > sprite.y:
                        orientation = 3
                    else:
                        orientation = 0
                sprite.makePortal(self.colour, orientation)
                self.destroy()
