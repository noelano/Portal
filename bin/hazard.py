from livewires import games
from utilities import LOC

class Hazard(games.Sprite):
    """
    Dangerous obstacle
    """
    image = games.load_image(LOC + r"\..\Images\hazard.bmp")

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Hazard, self).__init__(image = Hazard.image, x = x, y = y, dx = 0, dy = 0)
        self.game = game

    def update(self):
        """
        Check for objects falling into te hazard
        """

        for sprite in self.overlapping_sprites:
            if sprite == self.game.player:
                self.game.gameOver()