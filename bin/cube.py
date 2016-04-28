from livewires import games
from utilities import LOC, TERMINAL_VELOCITY, AIR_RESISTANCE, GRAVITY
from surfaces import *
from player import *
import math


class Cube(games.Sprite):
    """
    Companion cube
    """
    image = games.load_image(LOC + r"\..\Images\cube.bmp")
    total = 0

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Cube, self).__init__(image=Cube.image, x=x, y=y, dx=0, dy=0)
        self.game = game
        self.speed = 0
        self.counter = 0
        self.held = 0   # Keeps track of whether the cube is being held

    def update(self):
        """
        Act like a surface - user can stand on it and sentries can be blocked by it.
        Behaviour differs depending on whether it's being held or not
        """
        if self.counter > 0:
            self.counter -= 1
        else:
            self.checkForPickup()
            self.counter = 15

        self.freeUpdate()
        if self.held == 1:
            self.followPlayer()

        # Basic approximation of friction - if the cube is touching something, slow lateral movement
        if self.overlapping_sprites and self.held == 0:
            if self.dx > 0:
                self.dx -= 0.1
            elif self.dx < 0:
                self.dx += 0.1
            elif -0.1 <= self.dx <= 0.1:
                self.dx = 0

        self.calcSpeed()

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
        Cube.total -= 1
        self.destroy()

    def checkForPickup(self):
        """
        See if the player tries to pickup / put down the cube
        Note that this is only performed once every 15 frames
        Similar to checks in the text entry box
        """
        if self.game.player.reticule in self.overlapping_sprites and (games.keyboard.is_pressed(games.K_a) \
                or games.keyboard.is_pressed(games.K_d)):
            if self.held == 0:
                self.game.player.held_item = self
                self.held = 1
            else:
                self.game.player.held_item = None
                self.held = 0

    def freeUpdate(self):
        """ Standard update """
        if (not self.overlapping_sprites or set(self.overlapping_sprites).issubset(self.game.neutrinos)) \
                and self.dy < TERMINAL_VELOCITY and self.held == 0:
            self.dy += GRAVITY
            self.dx *= AIR_RESISTANCE

        # If the cube gets too far above / below the player, they have to drop it
        if self.held == 1 and (self.y > self.game.player.y + 30 or self.y < self.game.player.y - 30):
            self.held = 0
            self.game.player.held_item = None

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

    def followPlayer(self):
        """ Track the player"""
        if self.game.player.image in (Player.image1, Player.image2):
            self.left = self.game.player.right + 2
        else:
            self.right = self.game.player.left - 2
        self.dy = self.game.player.dy

