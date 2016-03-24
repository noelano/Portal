from livewires import games, color
from utilities import distance

class Exit(games.Sprite):
    """
    Exit location
    """
    image = games.load_image(r"Images\exit.bmp")

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Exit, self).__init__(image = Exit.image, x = x, y = y, dx = 0, dy = 0)
        self.game = game

    def update(self):
        """
        Check if the player has won
        """

        for sprite in self.overlapping_sprites:
            if sprite == self.game.player:
                if distance(self, sprite) < 10:
                    self.game.endPlayerGame()