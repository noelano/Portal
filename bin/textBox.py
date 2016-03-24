from livewires import games, color
import string
from utilities import LOC

class TextBox(games.Sprite):
    """
    Present a box to allow the user to input text
    Since text boxes don't exist in livewires a sprite is used as a workaround
    It's update method checks for the key presses and these are then displayed
    back using a text object
    """
    image = games.load_image(LOC + r"\..\Images\textBox.bmp")
    # Only alpha-numeric characters are allowed
    validChars = string.ascii_lowercase + string.digits

    def __init__(self, game, x, y):
        super(TextBox, self).__init__(image = TextBox.image, x = x, y = y, dx = 0, dy = 0)
        self.game = game
        self.text = ''
        self.counter = 0
        self.DisplayText = games.Text(value = '', size = 25, color = color.white,
                                top = self.y + 5, left = self.x - 20)
        games.screen.add(self.DisplayText)

    def update(self):
        """
        Accept text input from user and render on screen
        """
        self.counter += 1

        if self.counter % 13 == 0:
            if games.keyboard.is_pressed(games.K_RETURN) and self.text != '':
                self.game.fileName = "save\\" + self.text + ".dat"
                self.game.levelMenu()
            if games.keyboard.is_pressed(games.K_BACKSPACE):
                self.text = self.text[:-1]

            for char in TextBox.validChars:
                label = 'K_' + char
                # Check the attribute of the games object which matches label
                if games.keyboard.is_pressed(getattr(games, label)) and len(self.text) < 15:
                    self.text = self.text + char

        self.DisplayText.value = self.text.upper()