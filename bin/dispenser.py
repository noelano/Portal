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

    def dispense(self):
        """ Spawn a companion cube """
        cube = Cube(self.game, self.x, self.y + 80)
        games.screen.add(cube)
        self.game.cubes.append(cube)
