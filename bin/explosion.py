from livewires import games
from utilities import LOC

class Explosion(games.Animation):
    """ Explosion animation. """
    #sound = games.load_sound("explosion.wav")
    images = [LOC + "\\..\\Images\\explosion1.bmp",
              LOC + "\\..\\Images\\explosion2.bmp",
              LOC + "\\..\\Images\\explosion3.bmp",
              LOC + "\\..\\Images\\explosion4.bmp",
              LOC + "\\..\\Images\\explosion5.bmp",
              LOC + "\\..\\Images\\explosion6.bmp",
              LOC + "\\..\\Images\\explosion7.bmp",
              LOC + "\\..\\Images\\explosion8.bmp",
              LOC + "\\..\\Images\\explosion9.bmp"]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images = Explosion.images,
                                        x = x, y = y,
                                        repeat_interval = 4, n_repeats = 1,
                                        is_collideable = False)
        #Explosion.sound.play()