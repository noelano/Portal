from livewires import games, color
import math

games.init(screen_width = 1100, screen_height = 700, fps = 50)

class PortalShot(games.Sprite):
    """
    Object to create portal
    """

    image = games.load_image(r"Images\shot.bmp")

    def __init__(self, game, x, y, dx, dy, colour, shotype):
        """ Initialize the sprite. """
        velocityFactor = 0.8

        super(PortalShot, self).__init__(image = PortalShot.image, x = x, y = y, dx = velocityFactor * dx, dy = velocityFactor * dy)
        self.game = game
        self.lifetime = 30
        self.colour = colour
        self.shotype = shotype

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

                if self.shotype == 0:
                    if abs(self.x - sprite.bottom) < 3:
                        orientation = 3
                    else:
                        orientation = 2
                elif self.shotype == 1:
                    if abs(self.x - sprite.top) < 3:
                        orientation = 0
                    else:
                        orientation = 1
                elif self.shotype == 2:
                    if abs(self.x - sprite.bottom) < 3:
                        orientation = 3
                    else:
                        orientation = 1
                else:
                    if abs(self.x - sprite.top) < 3:
                        orientation = 0
                    else:
                        orientation = 2

                sprite.makePortal(self.colour, orientation)
                self.destroy()
