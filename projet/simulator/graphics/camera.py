from ..utils.vector import Vector2
from math import tan , sin, cos


class Camera:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.position = Vector2(0, 0)
        self.scale = 1

    def to_screen_coords(self, position):
        """ Converts the world-coordinate position to screen-coordinate. """
        theta = 30
        self.image = Vector2( position.getx + cos(thta)*position.gety, sin(theta)*position.gety )
        return image
        raise NotImplementedError

    def from_screen_coords(self, position):
        """ Converts the screen-coordinate position to a world-coordinate. """
        theta = 30
        self.image = Vector2( position.getx -position.gety/tan(theta) , position.gety/sin(theta) )
        return image
        raise NotImplementedError
