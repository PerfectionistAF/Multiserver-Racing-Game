# Enums
from enum import Enum


class GameState(Enum):
    MainMenu = 0
    GameSetup = 1
    GamePlay = 2
    GameEnd = 3


# Types
PlayerSnapshot = tuple[int, int, int]  # x, y, deg
GameSnapshot = list[PlayerSnapshot]
Movement = list[int, 2]  # Direction and Angle

# Helper Functions
import pickle


def getMovementData(data: str) -> Movement:
    return pickle.loads(data)


def dumpGameSnapshotData(data: GameSnapshot) -> bytes:
    return pickle.dumps(data)


# Constants
SPEED = 5
DEGREE = 3

GAME_SIZE = (800, 600)
UI_SIZE = 250
WINDOW_SIZE = (GAME_SIZE[0] + UI_SIZE, GAME_SIZE[1])

CTB_HIGHT = 500
ETB_HIGHT = 50
BTN_HIGHT = 50

HOST, PORT = "localhost", 8888