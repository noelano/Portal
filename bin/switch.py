from livewires import games
from utilities import LOC
from switchBase import *


class Switch(games.Sprite):
    """
    Button object that can be stepped on to open exit
    """
    image = games.load_image(LOC + r"\..\Images\switch_button.bmp")

    def __init__(self, game, exit, x, y):
        """ Initialize the sprite. """
        super(Switch, self).__init__(image=Switch.image, x=x, y=y, dx=0, dy=0)
        self.game = game
        self.exit = exit
        self.lowest_point = y + 11
        self.highest_point = y
        self.counter = 0

    def update(self):
        """ If someone steps on the switch it moves down """
        stepping_sprites = [x for x in self.overlapping_sprites if
                            x not in self.game.surfaces and x not in self.game.neutrinos]

        if self.counter != 0 and not stepping_sprites:
            self.counter -= 1

        if stepping_sprites:
            self.y = self.lowest_point
            self.exit.activate()

            # Want to delay the release of the switch by a second
            self.counter = 60

        elif self.counter == 0:
            self.y = self.highest_point
            self.exit.deactivate()

    def addBase(self):
        """ Create a base - want this to be overlayed on the button, hence it's not included in the init"""
        self.base = SwitchBase(self.game, self.x, self.y + 13)
        games.screen.add(self.base)
        self.game.surfaces.append(self.base)
