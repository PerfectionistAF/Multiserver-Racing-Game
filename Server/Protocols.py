# Enums
from enum import Enum
class GameState(Enum):
    MainMenu = 0
    GameSetup = 1
    GameLoop = 2
    GameEnd = 3

class Sign(Enum):
    Positive = 1
    Zero = 0
    Negative = -1

# Types
PlayerSnapshot = tuple[int,int,int] # x, y, deg
GameSnapshot = list[PlayerSnapshot]
Movement = list[int, 2] # Direction and Angle
from Server.Player import Player
PlayerList = dict[int, Player] # id, Player

# Constance
SPEED = 5
DEGREE = 3

TICK_RATE = 30