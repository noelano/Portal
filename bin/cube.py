from livewires import games
from utilities import LOC, TERMINAL_VELOCITY, AIR_RESISTANCE, GRAVITY
from surfaces import *
import math


class Cube(games.Sprite):
    """
    Companion cube
    """
    image = games.load_image(LOC + r"\..\Images\cube.bmp")

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Cube, self).__init__(image=Cube.image, x=x, y=y, dx=0, dy=0)
        self.game = game
        self.speed = 0

    def update(self):
        """ Act like a surface - user can stand on it and sentries can be blocked by it """
        if (not self.overlapping_sprites or set(self.overlapping_sprites).issubset(self.game.neutrinos)) \
                and self.dy < TERMINAL_VELOCITY:
            self.dy += GRAVITY
            self.dx *= AIR_RESISTANCE

        for sprite in self.overlapping_sprites:
            # Don't want to make changes to any other surfaces
            if sprite not in self.game.surfaces and sprite not in self.game.neutrinos:
                a = abs(self.bottom - sprite.top)
                b = abs(self.top - sprite.bottom)
                c = abs(self.left - sprite.right)
                d = abs(self.right - sprite.left)

                if sprite.dy >= 0:
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

    def handleLeft(self, sprite):
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

    def calcSpeed(self):
        self.speed = math.sqrt(self.dx**2 + self.dy**2)

    def die(self):
        self.destroy()
