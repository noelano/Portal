from livewires import games
from utilities import LOC
from dispenser import *


class Button(games.Sprite):
    """
    Button object that can be pressed to dispense companion cubes
    """
    image = games.load_image(LOC + r"\..\Images\button.bmp")

    def __init__(self, game, parent, x, y):
        """ Initialize the sprite. """
        super(Button, self).__init__(image=Button.image, x=x, y=y, dx=0, dy=0)
        self.game = game
        self.parent = parent
        self.counter = 0

    def update(self):
        """ If player is over the button they can press it """
        if self.counter != 0:
            self.counter -= 1       # Stops cubes from being continuously being spawned if button is held

        for sprite in self.overlapping_sprites:
            if sprite == self.game.player and games.keyboard.is_pressed(games.K_s) and self.counter == 0:
                self.parent.dispense()
                self.counter = 30
