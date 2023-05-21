# Enums
from enum import Enum
from typing import Any


class GameState(Enum):
    MainMenu = 0
    GameSetup = 1
    GamePlay = 2
    GameEnd = 3


# Types
PlayerSnapshot = tuple[int, int, int]  # x, y, deg
GameSnapshot = list[PlayerSnapshot]
Movement = list[int, 2]  # Direction and Angle
Packet = tuple[GameState, int | Movement]  # State and Data

# Helper Functions
import pickle


def getData(data: bytes) -> Packet:
    return pickle.loads(data)


def dumpData(data: Packet) -> bytes:
    return pickle.dumps(data)


# Constants
SPEED = 5
DEGREE = 3

TICK_RATE = 30
HOST, PORT = "localhost", 8888
MAX_PLAYERS = 4
