from math import sin, cos, radians

from Protocols import Movement, DEGREE, SPEED


class Player:
    def __init__(self, id: int) -> None:
        self.id = id
        self.x = 100.0
        self.y = 100.0 + id * 10
        self.deg = 0.0
        self.score = 0

    def move(self, movement: Movement) -> None:
        direction, angle = movement
        self.deg = self.deg + DEGREE * angle
        if self.deg < 0.0:
            self.deg += 360.0
        elif self.deg > 360.0:
            self.deg -= 360.0
        self.x += SPEED * cos(radians(self.deg)) * direction
        self.y -= SPEED * sin(radians(self.deg)) * direction
        self.score += 1
