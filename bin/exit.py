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
        self.counter = 0
        self.time = 0
        self.message = None

    def update(self):
        """
        Check if the player has won
        """
        self.counter += 1

        # Check for menu selection
        if games.keyboard.is_pressed(games.K_m):
            self.game.levelMenu()

        if self.counter % 25 == 0:
            # Update score and timer each half second
            self.time = int(self.counter / 50)

        # Check if the player has reached the exit
        for sprite in self.overlapping_sprites:
            if sprite == self.game.player:
                if distance(self, sprite) < 20 and not self.message:
                    message = games.Message(value = self.end_message,
                                    size = 30,
                                    color = color.white,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 2 * games.screen.fps,
                                    after_death = self.game.levelComplete)
                    self.message = message
                    games.screen.add(message)