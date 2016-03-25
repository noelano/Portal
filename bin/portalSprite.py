from livewires import games
from utilities import LOC
from surfaces import *

class PortalShot(games.Sprite):
    """
    Object to create portal
    """
    Lifetime = 50

    image = games.load_image(LOC + r"\..\Images\shot.bmp")

    def __init__(self, game, x, y, dx, dy, colour):
        """ Initialize the sprite. """
        velocityFactor = 0.7

        super(PortalShot, self).__init__(image = PortalShot.image, x = x, y = y, dx = velocityFactor * dx, dy = velocityFactor * dy)
        self.game = game
        self.lifetime = PortalShot.Lifetime
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
            if type(sprite) == Surface:
                orientation = 0

                # Calculate distances to determine where overlap is
                #a = abs(self.bottom - sprite.top)
                #b = abs(self.top - sprite.bottom)
                #c = abs(self.left - sprite.right)
                #d = abs(self.right - sprite.left)

                a = abs(self.y - sprite.top)
                b = abs(self.y - sprite.bottom)
                c = abs(self.x - sprite.right)
                d = abs(self.x - sprite.left)

                if a > b:
                    if c < b:
                        orientation = 2
                    elif d < b:
                        orientation = 1
                    else:
                        orientation = 3
                else:
                    if c < a:
                        orientation = 2
                    elif d < a:
                        orientation = 1
                    else:
                        orientation = 0

                sprite.makePortal(self.colour, orientation)
                self.destroy()
