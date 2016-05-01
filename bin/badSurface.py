from livewires import games
import random
from utilities import distance, LOC

class BadSurface(games.Sprite):
    """
    Acts like surface in relation to being solid. Can't create portals though
    """
    image1 = games.load_image(LOC + r"\..\Images\badSurface1.bmp")
    image2 = games.load_image(LOC + r"\..\Images\badSurface2.bmp")
    image3 = games.load_image(LOC + r"\..\Images\badSurface3.bmp")
    images = [image1, image2, image3]

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        picker = random.uniform(0,1)
        if picker > 0.4:
            self.choice = 0
        elif picker > 0.2:
            self.choice = 1
        else:
            self.choice = 2
        super(BadSurface, self).__init__(image = BadSurface.images[self.choice], x = x, y = y, dx = 0, dy = 0)
        self.game = game

    def update(self):
        """
        The update won't affect this object but will be used to prevent anything from interacting with it
        """

        for sprite in self.overlapping_sprites:
            # Don't want to make changes to any other surfaces
            if (sprite not in self.game.surfaces and sprite not in self.game.neutrinos):
                #print(Surface.orangePortal, Surface.bluePortal, self, self.colour, self.orientation)

                # Calculate distances to determine where overlap is
                a = abs(self.bottom - sprite.top)
                b = abs(self.top - sprite.bottom)
                c = abs(self.left - sprite.right)
                d = abs(self.right - sprite.left)

                if sprite.dy > 0:
                    if c < min(a, b):
                        self.handleLeft(sprite)
                    elif d < min(a, b):
                        self.handleRight(sprite)
                    elif a > b:
                        self.handleTop(sprite)
                    else:
                        self.handleBottom(sprite)
                elif sprite.dy < 0 and b > a:
                    if c < a:
                        self.handleLeft(sprite)
                    elif d < a:
                        self.handleRight(sprite)
                    else:
                        self.handleBottom(sprite)
                elif c > d and b > 3:
                    self.handleRight(sprite)
                elif d > c and b > 3:
                    self.handleLeft(sprite)

    def handleLeft(self,sprite):
        sprite.dx = 0
        sprite.right = self.left - 1

    def handleRight(self, sprite):
        sprite.dx = 0
        sprite.left = self.right + 1

    def handleTop(self, sprite):
        sprite.dy = 0
        sprite.bottom = self.top + 1

    def handleBottom(self, sprite):
        sprite.dy = 0
        sprite.top = self.bottom
