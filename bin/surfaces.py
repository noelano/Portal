from livewires import games, color

class Surface(games.Sprite):
    """
    Pointer for highlighting and making selections on the game menus
    """
    image = games.load_image(r"Images\surface.bmp")

    def __init__(self, game, x, y):
        """ Initialize the sprite. """
        super(Surface, self).__init__(image = Surface.image, x = x, y = y, dx = 0, dy = 0)
        self.game = game

    def update(self):
        """
        The update won't affect this object but will be used to prevent anything from interacting with it
        """

        for sprite in self.overlapping_sprites:
            if (sprite.x > self.x and sprite.x < self.x + 80):
                if sprite.y < self.y - 40:
                    sprite.y = self.y - 80
                    sprite.dy = 0
