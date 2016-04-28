from livewires import games
from utilities import LOC
from button import *
from surfaces import *
from cube import *


class Dispenser(Surface):
    """
    Chute to dispense companion cubes
    """
    dispenser_image = games.load_image(LOC + r"\..\Images\dispenser.bmp")

    def __init__(self, game, x, y, button_x, button_y):
        """ Initialize the sprite. """
        super(Dispenser, self).__init__(game, x=x, y=y)
        self.exposedFaces = [1, 2]
        self.button = Button(self.game, self, button_x, button_y)
        games.screen.add(self.button)
        self.game.neutrinos.append(self.button)
        self.image = Dispenser.dispenser_image
        self.delay = 0   # Prevents too many cubes from being spawned too quickly

    def dispense(self):
        """ Spawn a companion cube """
        if self.delay == 0 and Cube.total < 5:
            cube = Cube(self.game, self.x, self.y + 80)
            games.screen.add(cube)
            Cube.total += 1
            self.game.cubes.append(cube)
            self.delay = 50

    def update(self):
        if self.delay != 0:
            self.delay -= 1
