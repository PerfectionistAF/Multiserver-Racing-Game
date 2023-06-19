# Types
PlayerSnapshot = list[float, float, float, int]  # x, y, deg, score
GameSnapshot = list[PlayerSnapshot]
Movement = list[int, int]  # Direction and Angle
Address = tuple[str, int]  # Host and Port


# Helper Functions
from pickle import dumps


def _singed_byte(b: int):
    return b - 256 if b >= 128 else b


def getData(data: bytes) -> Movement:
    return [_singed_byte(data[0]), _singed_byte(data[1])]


def dumpData(data: GameSnapshot) -> bytes:
    # return b''.join(
    #     [
    #         int.to_bytes(i, 4, signed=True)
    #         for playerSnapshot in data
    #         for i in playerSnapshot
    #     ]
    # )
    return dumps(data)


# Constants
SPEED = 5
DEGREE = 3

TICK_RATE = 30 / 1000
GAME_TIME = 60
QUEUE_MAX_TIME = 10

HOST, PORT = 'localhost', 8888
MAX_PLAYERS = 4
