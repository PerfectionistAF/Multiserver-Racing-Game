from math import sin, cos, radians
from Server.Protocols import *

class Game(object):
    def __init__(self) -> None:
        self.l_players:PlayerList

    def move(self, movement: Movement, id) -> None:
        direction, angle = movement
        player:Player = self.l_players[id]
        angle = player.deg + DEGREE*angle
        if angle < 0:
            angle += 360
        elif angle > 360:
            angle -= 360
        player.x += SPEED*cos(radians(angle))*direction
        player.y -= SPEED*sin(radians(angle))*direction
