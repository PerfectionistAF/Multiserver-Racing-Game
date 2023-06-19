from math import sin, cos, radians

from Protocols import Movement, DEGREE, SPEED
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
        self.score += 1
        #SQLITE 3 DB
        #Server id =1
        #Case: SERVER.PLAYER 
        #Player state = GameState
        #Player id
        #SQLITE 3 DB
        db = sqlite3.connect('move.sqlite')
        db.execute('CREATE TABLE IF NOT EXISTS Server_Players(Server_ID INTEGER, Client_ID INTEGER, X INTEGER, Y INTEGER, DEGREE INTEGER)')
        db.execute(f"INSERT INTO Server_Players(Server_ID, Client_ID, X, Y, DEGREE) VALUES('1', {self.id}, {self.x}, {self.y}, {self.deg})")
        db.commit()
        db.close()