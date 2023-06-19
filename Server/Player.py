from math import sin, cos, radians

from Protocols import Movement, DEGREE, SPEED
from Client.Protocols import GAME_SIZE, UI_SIZE, WINDOW_SIZE
import sqlite3

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
        if self.x > WINDOW_SIZE[0]:
            self.x -= UI_SIZE
        elif self.x < WINDOW_SIZE[0]:
            self.x += UI_SIZE
        self.y -= SPEED * sin(radians(self.deg)) * direction
        if self.y > WINDOW_SIZE[1]:
            self.y -= UI_SIZE
        elif self.y < WINDOW_SIZE[1]:
            self.y += UI_SIZE
        self.score += 1
        #SQLITE 3 DB
        #Server id =1
        #Case: SERVER.PLAYER 
        #Player state = GameState
        #Player id
