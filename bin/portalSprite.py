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
                orientation = None

                # Based on the direction the missile is travelling, determine what possible face is hit

                if self.dx > 0 and self.dy > 0:
                    if 0 in sprite.exposedFaces and 1 in sprite.exposedFaces:
                        # calculate closest
                        a = abs(self.y - sprite.top)
                        b = abs(self.x - sprite.left)
                        if a < b:
                            orientation = 0
                        else:
                            orientation = 1
                    elif 0 in sprite.exposedFaces:
                        orientation = 0
                    elif 1 in sprite.exposedFaces:
                        orientation = 1

                elif self.dx > 0 and self.dy < 0:
                    if 1 in sprite.exposedFaces and 3 in sprite.exposedFaces:
                        # calculate closest
                        a = abs(self.y - sprite.bottom)
                        b = abs(self.x - sprite.left)
                        if a < b:
                            orientation = 3
                        else:
                            orientation = 1
                    elif 1 in sprite.exposedFaces:
                        orientation = 1
                    elif 3 in sprite.exposedFaces:
                        orientation = 3

                elif self.dx < 0 and self.dy > 0:
                    if 0 in sprite.exposedFaces and 2 in sprite.exposedFaces:
                        # calculate closest
                        a = abs(self.y - sprite.top)
                        b = abs(self.x - sprite.right)
                        if a < b:
                            orientation = 0
                        else:
                            orientation = 2
                    elif 0 in sprite.exposedFaces:
                        orientation = 0
                    elif 2 in sprite.exposedFaces:
                        orientation = 2

                elif self.dx < 0 and self.dy < 0:
                    if 2 in sprite.exposedFaces and 3 in sprite.exposedFaces:
                        # calculate closest
                        a = abs(self.y - sprite.bottom)
                        b = abs(self.x - sprite.right)
                        if a < b:
                            orientation = 3
                        else:
                            orientation = 2
                    elif 2 in sprite.exposedFaces:
                        orientation = 2
                    elif 3 in sprite.exposedFaces:
                        orientation = 3

                elif self.dx > 0:
                    if 1 in sprite.exposedFaces:
                        orientation = 1

                elif self.dx < 0:
                    if 2 in sprite.exposedFaces:
                        orientation = 2

                elif self.dy > 0:
                    if 0 in sprite.exposedFaces:
                        orientation = 0

                elif self.dy < 0:
                    if 3 in sprite.exposedFaces:
                        orientation = 3

                if orientation != None:
                    sprite.makePortal(self.colour, orientation)
                self.destroy()

            elif sprite in self.game.surfaces:
                self.destroy()
