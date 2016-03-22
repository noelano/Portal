from livewires import games, color

games.init(screen_width = 1100, screen_height = 700, fps = 50)

class PortalHalo(games.Sprite):
    """
    Portal object
    """
    portalo = games.load_image(r"Images\portalo.bmp")
    #portalb = games.load_image(r"Images\portalb.bmp")

    def __init__(self, game, x, y, menu):
        """ Initialize the sprite. """
        super(PortalHalo, self).__init__(image = PortalHalo.portalo, x = x, y = y, dx = 0, dy = 0)
        self.game = game
        self.twin = None

    def update(self):
        """
        Move the pointer up and down through the options list
        If the user hits enter proceed with the selected option
        """
        self.counter += 1

        # Because we have 50 fps a single button press could lead to a number
        # of updates ie one press of 'up' could scroll up 6 times.
        # To prevent this we add a buffer of 10 frames, which is what the counter
        # variable is used for

        if self.counter % 13 == 0:
            if self.num_options > 0:
                if games.keyboard.is_pressed(games.K_UP):
                    self.move(-1)
                if games.keyboard.is_pressed(games.K_DOWN):
                    self.move(1)
            if games.keyboard.is_pressed(games.K_RETURN):
                self.enter()
