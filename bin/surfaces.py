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

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Surface, self).__init__(image = random.choice(Surface.images), x = x, y = y, dx = 0, dy = 0)
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
            if (sprite not in self.game.surfaces and sprite not in self.game.reticule):

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