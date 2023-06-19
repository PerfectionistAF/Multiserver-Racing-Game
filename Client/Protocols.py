# Enums
from enum import Enum


class GameState(Enum):
    MainMenu = 0
    GameSetup = 1
    GamePlay = 2
    GameEnd = 3


from pygame import Color


COLORS: tuple[str] = (
    '#e10909',  # Red
    '#3a749a',  # Blue
    '#16ad27',  # Green
    '#eadf05',  # Yellow
)


# Types
PlayerSnapshot = list[float, float, float, int]  # x, y, deg, score
GameSnapshot = list[PlayerSnapshot]
Movement = list[int, int]  # Direction and Angle
Address = tuple[str, int]  # Host and Port


# Helper Functions
from pickle import loads


def getData(data: bytes) -> GameSnapshot:
    return loads(data)
    # return [
    #     [
    #         int.from_bytes(data[(i * 4) + j : (i * 4) + j + 4], signed=True)
    #         for i in range(3)
    #     ]
    #     for j in range(0, len(data), 4 * 3)
    # ]


def dumpData(data: Movement) -> bytes:
    return b''.join(
        [
            int.to_bytes(data[0], length=1, byteorder='big', signed=True),
            int.to_bytes(data[1], length=1, byteorder='big', signed=True),
        ]
    )


def decodeMessage(data: bytes) -> tuple[str, str]:
    message = data.decode(errors='ignore')
    return message[0], message[1:]


# Constants
SPEED = 5
DEGREE = 3

GAME_SIZE = (800, 600)
UI_SIZE = 250
WINDOW_SIZE = (GAME_SIZE[0] + UI_SIZE, GAME_SIZE[1])

CTB_HIGHT = 500
ETB_HIGHT = 50
BTN_HIGHT = 50

HOST, PORT = '13.51.142.74', 8888
MAX_PLAYERS = 4

TEXT_SIZE = 30
TEXT_SPACE = (GAME_SIZE[0] - (MAX_PLAYERS * TEXT_SIZE)) / (MAX_PLAYERS + 1)
