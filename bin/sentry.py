from livewires import games
from sentryLOS import *
from laser import *
from explosion import *
import math, random
from utilities import LOC, GRAVITY, TERMINAL_VELOCITY, AIR_RESISTANCE


class Sentry(games.Sprite):
    """ Enemy sentry. Moves randomly and shoots lasers if player is spotted """

    image1 = games.load_image(LOC + r"\..\Images\sentry1.bmp")
    image2 = games.load_image(LOC + r"\..\Images\sentry2.bmp")
    image3 = games.load_image(LOC + r"\..\Images\sentry3.bmp")
    image4 = games.load_image(LOC + r"\..\Images\sentry4.bmp")

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Sentry, self).__init__(image=Sentry.image1, x=x, y=y, dx=0, dy=0)
        self.game = game
        self.counter = 0    # To control the refresh of the sprite image
        self.speed = 0
        self.direction = 1

    def update(self):
        """
        Move randomly. If the sprite is already moving the probability to keep moving is higher
        Prevents a 'jittery' looking motion.

        Also spawn a line of sight object to 'look' for other sprites. If any are seen, shoot at them
        """
        self.counter += 1
        self.calcSpeed()

        if not self.overlapping_sprites and self.dy < TERMINAL_VELOCITY:
            self.dy += GRAVITY
            self.dx *= AIR_RESISTANCE

        # Every half second spawn an LOS object to 'look'
        if self.counter % 25 == 0:
            self.look()

        # As long as the sprite is not falling, move randomly to left or right
        if self.dy == 0 and self.counter % 50 == 0:
            selector = random.uniform(0.0, 1.0)

            if self.dx == 0:
                if selector > 0.8:
                    self.dx = 1
                    self.direction = 1
                    if self.image in (Sentry.image3, Sentry.image4):
                        self.image = Sentry.image1
                elif selector > 0.6:
                    self.dx = -1
                    self.direction = -1
                    if self.image in (Sentry.image1, Sentry.image2):
                        self.image = Sentry.image3
            elif self.dx > 0:
                if selector > 0.8:
                    self.dx = -1
                    self.direction = -1
                    if self.image in (Sentry.image1, Sentry.image2):
                        self.image = Sentry.image3
                elif selector > 0.6:
                    self.dx = 0
            elif self.dx < 0:
                if selector > 0.8:
                    self.dx = 1
                    self.direction = 1
                    if self.image in (Sentry.image3, Sentry.image4):
                        self.image = Sentry.image1
                elif selector > 0.6:
                    self.dx = 0

        # Alternate between each image while moving to animate the sprite
        if self.dx > 0 and self.dy == 0:
            if self.counter % 30 == 0:
                self.image = Sentry.image2
            elif self.counter % 15 == 0:
                self.image = Sentry.image1
        elif self.dx < 0 and self.dy == 0:
            if self.counter % 30 == 0:
                self.image = Sentry.image3
            elif self.counter % 15 == 0:
                self.image = Sentry.image4

    def calcSpeed(self):
        self.speed = math.sqrt(self.dx**2 + self.dy**2)

    def die(self):
        new_explosion = Explosion(x=self.x, y=self.y)
        games.screen.add(new_explosion)
        self.destroy()

    def look(self):
        if self.direction == 1:
            sight = SentryLOS(self.game, self, self.right + 1, self.y, 24)
        else:
            sight = SentryLOS(self.game, self, self.left - 1, self.y, -24)
        games.screen.add(sight)
        self.game.neutrinos.append(sight)

    def shootLaser(self):
        if self.direction == 1:
            laser = Laser(self.game, self.right + 16, self.y, 12)
        else:
            laser = Laser(self.game, self.left - 16, self.y, -12)
        games.screen.add(laser)
        self.game.neutrinos.append(laser)