from livewires import games
import random, pygame
from utilities import distance, LOC

games.init(screen_width = 1100, screen_height = 700, fps = 50)
pygame.display.set_mode((1100,700),pygame.FULLSCREEN)


class Surface(games.Sprite):
    """
    Surface that portals can be shot onto
    """
    image1 = games.load_image(LOC + r"\..\Images\surface1.bmp")
    image2 = games.load_image(LOC + r"\..\Images\surface2.bmp")
    image3 = games.load_image(LOC + r"\..\Images\surface3.bmp")
    images = [image1, image2, image3]
    orange1 = games.load_image(LOC + r"\..\Images\orange1.bmp")
    orange2 = games.load_image(LOC + r"\..\Images\orange2.bmp")
    orange3 = games.load_image(LOC + r"\..\Images\orange3.bmp")
    orange4 = games.load_image(LOC + r"\..\Images\orange4.bmp")
    oranges = [orange1, orange2, orange3, orange4]
    blue1 = games.load_image(LOC + r"\..\Images\blue1.bmp")
    blue2 = games.load_image(LOC + r"\..\Images\blue2.bmp")
    blue3 = games.load_image(LOC + r"\..\Images\blue3.bmp")
    blue4 = games.load_image(LOC + r"\..\Images\blue4.bmp")
    blues = [blue1, blue2, blue3, blue4]

    orangePortal = None
    bluePortal = None

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        self.choice = random.randint(0,2)
        super(Surface, self).__init__(image=Surface.images[self.choice], x=x, y=y, dx=0, dy=0)
        self.game = game
        self.orientation = -1
        self.colour = -1
        self.exposedFaces = [0,1,2,3]

    def update(self):
        """
        The update won't affect this object but will be used to prevent anything from interacting with it
        """

        for sprite in self.overlapping_sprites:
            # Don't want to make changes to any other surfaces
            if sprite not in self.game.surfaces and sprite not in self.game.neutrinos:

                # Calculate distances to determine where overlap is
                a = abs(self.bottom - sprite.top)
                b = abs(self.top - sprite.bottom)
                c = abs(self.left - sprite.right)
                d = abs(self.right - sprite.left)

                if self.orientation == 0 and sprite.dy > 0:
                    self.handleTop(sprite)

                elif sprite.dy >= 0:
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

    def makePortal(self, colour, orientation):
        """
        Transform into a portal
        """

        # First check if we're already set as a portal
        if self.colour != -1:
            self.clearPortal()

        if colour == 0:
            if Surface.orangePortal:
                Surface.orangePortal.clearPortal()
            self.image = Surface.oranges[orientation]
            Surface.orangePortal = self
        elif colour == 1:
            if Surface.bluePortal:
                Surface.bluePortal.clearPortal()
            self.image = Surface.blues[orientation]
            Surface.bluePortal = self

        self.orientation = orientation
        self.colour = colour

    def clearPortal(self):
        self.image = Surface.images[self.choice]
        self.orientation = -1
        if self.colour == 0:
            Surface.orangePortal = None
        elif self.colour == 1:
            Surface.bluePortal = None
        self.colour = -1

    def handleLeft(self,sprite):
        if self.orientation == 1 and Surface.bluePortal and Surface.orangePortal:
            if distance(self, sprite) < 10:
                if self.colour == 0:
                    self.teleportBlue(sprite)
                else:
                    self.teleportOrange(sprite)
        else:
            sprite.dx = 0
            sprite.right = self.left - 1

    def handleRight(self, sprite):
        if self.orientation == 2 and Surface.bluePortal and Surface.orangePortal:
            if distance(self, sprite) < 10:
                if self.colour == 0:
                    self.teleportBlue(sprite)
                else:
                    self.teleportOrange(sprite)
        else:
            sprite.dx = 0
            sprite.left = self.right + 1

    def handleTop(self, sprite):
        if self.orientation == 0 and Surface.bluePortal and Surface.orangePortal and abs(self.x - sprite.x) < 30:
            sprite.x = self.x
            if sprite.dy == 0:
                sprite.dy += 0.5
            if distance(self, sprite) < 10:
                if self.colour == 0:
                    self.teleportBlue(sprite)
                else:
                    self.teleportOrange(sprite)
        else:
            sprite.dy = 0
            sprite.bottom = self.top + 1

    def handleBottom(self, sprite):
        if self.orientation == 3 and Surface.bluePortal and Surface.orangePortal:
            sprite.dy += 0.02
            if distance(self, sprite) < 10:
                if self.colour == 0:
                    self.teleportBlue(sprite)
                else:
                    self.teleportOrange(sprite)
        else:
            sprite.dy = 0
            sprite.top = self.bottom

    def teleportBlue(self, sprite):

        if Surface.bluePortal.orientation == 0:
            sprite.x = Surface.bluePortal.x
            sprite.y = Surface.bluePortal.y - 11
            # To prevent player constantly falling into two holes
            if self.orientation != 0 or sprite.speed > 0.8:
                sprite.dx = 0
                sprite.dy = -sprite.speed
            else:
                sprite.dx = 1
                sprite.dy = -1

        elif Surface.bluePortal.orientation == 1:
            sprite.x = Surface.bluePortal.x - 11
            sprite.bottom = Surface.bluePortal.bottom - 3
            sprite.dy = 0.02
            sprite.dx = -sprite.speed
        elif Surface.bluePortal.orientation == 2:
            sprite.x = Surface.bluePortal.x + 11
            sprite.bottom = Surface.bluePortal.bottom - 3
            sprite.dy = 0.02
            sprite.dx = sprite.speed
        else:
            sprite.x = Surface.bluePortal.x
            sprite.y = Surface.bluePortal.y + 11
            sprite.dx = 0
            sprite.dy = sprite.speed

    def teleportOrange(self, sprite):

        if Surface.orangePortal.orientation == 0:
            sprite.x = Surface.orangePortal.x
            sprite.y = Surface.orangePortal.y - 11
            # To prevent player constantly falling into two holes
            if self.orientation != 0 or sprite.speed > 0.7:
                sprite.dx = 0
                sprite.dy = -sprite.speed
            else:
                sprite.dx = 1
                sprite.dy = -1
        elif Surface.orangePortal.orientation == 1:
            sprite.x = Surface.orangePortal.x - 11
            sprite.bottom = Surface.orangePortal.bottom - 3
            sprite.dy = 0.02
            sprite.dx = -sprite.speed
        elif Surface.orangePortal.orientation == 2:
            sprite.x = Surface.orangePortal.x + 11
            sprite.bottom = Surface.orangePortal.bottom - 3
            sprite.dy = 0.02
            sprite.dx = sprite.speed
        else:
            sprite.x = Surface.orangePortal.x
            sprite.y = Surface.orangePortal.y + 11
            sprite.dx = 0
            sprite.dy = sprite.speed

    def calculateExposedFaces(self):
        """
        Determine which faces are exposed. Portals can only be placed on these faces
        This is done by checking the overlapping sprites to see which sides have an overlap
        (And are therefore not exposed)
        """

        for sprite in self.overlapping_sprites:
            a = abs(self.bottom - sprite.top)
            b = abs(self.top - sprite.bottom)
            c = abs(self.left - sprite.right)
            d = abs(self.right - sprite.left)
            e = abs(self.left - sprite.left)
            f = abs(self.bottom - sprite.bottom)

            if b < a and (e < 55):
                if 0 in self.exposedFaces:
                    self.exposedFaces.remove(0)
            if a < b and (e < 55):
                if 3 in self.exposedFaces:
                    self.exposedFaces.remove(3)
            if c < d and (f < 55):
                if 1 in self.exposedFaces:
                    self.exposedFaces.remove(1)
            if d < c and (f < 55):
                if 2 in self.exposedFaces:
                    self.exposedFaces.remove(2)
