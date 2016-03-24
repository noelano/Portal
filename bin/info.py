# Text object for displaying messages

from livewires import games, color

class Info(games.Text):
    def __init__(self, message, size, colour, x, y, lifetime, dx = 0, dy = 0):
        """ Initialize the sprite. """
        super(Info, self).__init__(value = message, size = size, color = colour, x = x, y = y, dx = dx, dy = dy)
        self.lifetime = lifetime

    def update(self):
        """
        Check if the player has won
        """

        if self.lifetime <= 0:
            self.destroy()
        else:
            self.lifetime -= 1
