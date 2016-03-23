from livewires import games, color
import random

class Surface(games.Sprite):
    """
    Pointer for highlighting and making selections on the game menus
    """
    image1 = games.load_image(r"Images\surface1.bmp")
    image2 = games.load_image(r"Images\surface2.bmp")
    image3 = games.load_image(r"Images\surface3.bmp")
    images = [image1, image2, image3]
    orange1 = games.load_image(r"Images\orange1.bmp")
    orange2 = games.load_image(r"Images\orange2.bmp")
    orange3 = games.load_image(r"Images\orange3.bmp")
    orange4 = games.load_image(r"Images\orange4.bmp")
    oranges = [orange1, orange2, orange3, orange4]
    blue1 = games.load_image(r"Images\blue1.bmp")
    blue2 = games.load_image(r"Images\blue2.bmp")
    blue3 = games.load_image(r"Images\blue3.bmp")
    blue4 = games.load_image(r"Images\blue4.bmp")
    blues = [blue1, blue2, blue3, blue4]

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        self.choice = random.randint(0,2)
        super(Surface, self).__init__(image = Surface.images[self.choice], x = x, y = y, dx = 0, dy = 0)
        self.game = game
        self.bottom = y + 40
        self.top = y - 40
        self.left = x - 40
        self.right = x + 40
        self.portal = 0     # Used for transforming into portal

    def update(self):
        """
        The update won't affect this object but will be used to prevent anything from interacting with it
        """

        for sprite in self.overlapping_sprites:
            # Don't want to make changes to any other surfaces
            if (sprite not in self.game.surfaces and sprite not in self.game.neutrinos):

                if self.portal == 0:
                    # Calculate distances to determine where overlap is
                    a = abs(self.bottom - sprite.top)
                    b = abs(self.top - sprite.bottom)
                    c = abs(self.left - sprite.right)
                    d = abs(self.right - sprite.left)

                    if sprite.dy > 0:
                        if a > b:
                            sprite.dy = 0
                            sprite.bottom = self.top + 1
                        elif b > a:
                            sprite.dy = 0
                            sprite.top = self.bottom
                    elif c > d and b > 3:
                        sprite.dx = 0
                        sprite.left = self.right + 1
                    elif d > c and b > 3:
                        sprite.dx = 0
                        sprite.right = self.left - 1

                else:
                    # In this case the surface acts as a portal
                    sprite.x = 0

    def makePortal(self, colour, orientation):
        """
        Transform into a portal
        """

        if colour == 0:
            if self.game.orange:
                self.game.orange.clearPortal()
            self.image = Surface.oranges[orientation]
            self.game.orange = self
        elif colour == 1:
            if self.game.blue:
                self.game.blue.clearPortal()
            self.image = Surface.blues[orientation]
            self.game.blue = self

    def clearPortal(self):
        self.image = Surface.images[self.choice]