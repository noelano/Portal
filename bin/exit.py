from livewires import games, color
from utilities import distance, LOC
from switch import *

class Exit(games.Sprite):
    """
    Exit location
    """
    image1 = games.load_image(LOC + r"\..\Images\exit.bmp")
    image2 = games.load_image(LOC + r"\..\Images\exit_inactive.bmp")

    def __init__(self, game, end_message, x, y, has_button=0, button_x=0, button_y=0):
        """ Initialize the sprite. """
        super(Exit, self).__init__(image=Exit.image1, x=x, y=y, dx=0, dy=0)
        self.game = game
        self.end_message = end_message
        self.counter = 0
        self.time = 0
        self.message = None
        if has_button:
            self.active = 0
            self.image = Exit.image2
            self.button = Switch(self.game, self, x=button_x, y=button_y)
            games.screen.add(self.button)
            self.game.neutrinos.append(self.button)
            self.button.addBase()
        else:
            self.active = 1

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
            if sprite == self.game.player and self.active:
                if distance(self, sprite) < 20 and not self.message:
                    message = games.Message(value=self.end_message,
                                    size=30,
                                    color=color.white,
                                    x=games.screen.width/2,
                                    y=games.screen.height/2,
                                    lifetime=2 * games.screen.fps,
                                    after_death=self.game.levelComplete)
                    self.message = message
                    games.screen.add(message)

    def activate(self):
        self.image = Exit.image1
        self.active = 1

    def deactivate(self):
        self.image = Exit.image2
        self.active = 0
