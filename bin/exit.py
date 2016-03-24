from livewires import games, color
from utilities import distance, LOC

class Exit(games.Sprite):
    """
    Exit location
    """
    image = games.load_image(LOC + r"\..\Images\exit.bmp")

    def __init__(self, game, end_message, x, y):
        """ Initialize the sprite. """
        super(Exit, self).__init__(image = Exit.image, x = x, y = y, dx = 0, dy = 0)
        self.game = game
        self.end_message = end_message

    def update(self):
        """
        Check if the player has won
        """

        for sprite in self.overlapping_sprites:
            if sprite == self.game.player:
                if distance(self, sprite) < 20:
                    message = games.Message(value = self.end_message,
                                    size = 60,
                                    color = color.blue,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 2 * games.screen.fps,
                                    after_death = self.game.levelComplete)
                    games.screen.add(message)