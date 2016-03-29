from livewires import games, color
from utilities import LOC


class MenuPointer(games.Sprite):
    """
    Pointer for highlighting and making selections on the game menus
    """
    image = games.load_image(LOC + r"\..\Images\pointer.bmp")

    def __init__(self, game, x, y, menu):
        """ Initialize the sprite. """
        super(MenuPointer, self).__init__(image=MenuPointer.image, x=x, y=y, dx=0, dy=0)
        self.game = game
        self.selection = 0
        self.num_options = len(self.game.options) - 1
        self.menu = menu
        self.counter = 15

    def update(self):
        """
        Move the pointer up and down through the options list
        If the user hits enter proceed with the selected option
        """
        if self.counter > 0:
            self.counter -= 1

        # Because we have 50 fps a single button press could lead to a number
        # of updates ie one press of 'up' could scroll up 6 times.
        # To prevent this we add a buffer of 10 frames, which is what the counter
        # variable is used for

        if self.counter == 0:
            if self.num_options > 0:
                if games.keyboard.is_pressed(games.K_UP):
                    self.counter = 15
                    self.move(-1)
                if games.keyboard.is_pressed(games.K_DOWN):
                    self.counter = 15
                    self.move(1)
            if games.keyboard.is_pressed(games.K_RETURN):
                self.counter = 15
                self.enter()

    def move(self, dir):
        """
        Move the pointer in the list based on the input direction 'dir'
        """
        old_selection = self.selection
        self.selection += dir

        # Check if we've gone beyond top of list and move to bottom
        # Likewise, go to the top if we move beyond the bottom
        if self.selection < 0:
            self.selection = self.num_options
        elif self.selection > self.num_options:
            self.selection = 0

        # Get y location of newly selected option
        y_location = self.game.options[self.selection].y
        x_location = self.game.options[self.selection].left

        # Put the pointer at this location
        self.y = y_location
        self.right = x_location - 4

        # Change option colours
        self.game.options[old_selection].color = color.white
        self.game.options[self.selection].color = color.blue

    def enter(self):
        """
        Perform an action based on the selected menu option
        """

        if self.menu == 0:
            if self.selection == 0:
                #self.game.loadGame()
                # For quick testing:
                self.game.Level(13, self.game.fileName)
            elif self.selection == 1:
                self.game.tutorial()
            else:
                games.screen.quit()
        elif self.menu == 1:
            # The selection is a file name.
            # get the label from the game object and proceed to next menu
            if self.selection == self.num_options:
                self.game.homescreen()
            else:
                fileName = self.game.options[self.selection].value
                if fileName == 'NEW GAME':
                    fileName = self.game.enterName()
                else:
                    fileName = "save\\" + fileName + ".dat"
                    self.game.fileName = fileName
                    self.game.levelMenu()
        elif self.menu == 2:
            # Choose a level
            if self.selection == self.num_options:
                self.game.loadGame()
            else:
                level = int(self.selection)
                self.game.Level(level, self.game.fileName)
