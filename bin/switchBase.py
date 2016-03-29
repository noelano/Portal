from livewires import games
from utilities import LOC


class SwitchBase(games.Sprite):
    """
    Base of switch
    """
    image = games.load_image(LOC + r"\..\Images\switch_base.bmp")

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(SwitchBase, self).__init__(image=SwitchBase.image, x=x, y=y, dx=0, dy=0)
        self.game = game

    def update(self):
        """ If someone steps on the base, put them on top of it """

        for sprite in self.overlapping_sprites:
            if sprite not in self.game.surfaces and sprite not in self.game.neutrinos:
                sprite.bottom = self.top + 1
                if sprite.dy > 0:
                    sprite.dy = 0
