# Types
PlayerSnapshot = tuple[int, int, int]  # x, y, deg
GameSnapshot = list[PlayerSnapshot]
Movement = list[int, 2]  # Direction and Angle
Address = tuple[str, int]  # Host and Port

# Helper Functions
from pickle import loads, dumps


def getData(data: bytes) -> Movement:
    return loads(data)


def dumpData(data: GameSnapshot) -> bytes:
    return dumps(data)


# Constants
SPEED = 5
DEGREE = 3

TICK_RATE = 30 / 1000
GAME_TIME = 90

HOST, PORT = 'localhost', 8888
MAX_PLAYERS = 4
