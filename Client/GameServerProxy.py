from math import sin, cos, radians
from pygame import sprite, Surface, image, transform

from Player import Player
from Protocols import GAME_SIZE, DEGREE, SPEED, GameState, GameSnapshot, Movement


class Game(object):
    def __init__(self) -> None:
        self.LatestSnapshot: GameSnapshot = GameSnapshot
        self.State: GameState = GameState.MainMenu
        self.l_players: list[Player] = []
        self.g_players = sprite.RenderClear()
        self.map = image.load("./Sprites/Map.png").convert()
        self.map = transform.scale(self.map, GAME_SIZE)

    # TO-DO: Receive snapshot from GameServer and update the LatestSnapshot
    def getSnapshot(self) -> None:
        self.LatestSnapshot = [(100, 100, 0)]

    def update(self, screen: Surface, movement: Movement) -> None:
        match self.State:
            case GameState.MainMenu:
                screen.blit(self.map, (0, 0))
                self.State = GameState.GameSetup
                # TO-DO: Setup a Socket to connect to a game
            case GameState.GameSetup:
                self.getSnapshot()  # starts a Thread+Socket to continuously receive the LatestSnapshot
                self.id = 0  # TO-DO: get this Game instance's id from server
                for i in range(len(self.LatestSnapshot)):
                    self.createPlayer(i)
                # TO-DO: Create x number of Players as decreed by the GameServer
                self.State = GameState.GamePlay
            case GameState.GamePlay:
                self.g_players.update(self.LatestSnapshot)
                self.g_players.clear(screen, self.map)
                self.g_players.draw(screen)
                self.move(movement)
                # TO-DO: listen to GameServer for winner and go to the next State
            case GameState.GameEnd:
                pass

    def createPlayer(self, id) -> None:
        # TO-DO: get id of other players and create players
        newPlayer = Player(id)
        self.l_players.append(newPlayer)
        self.g_players.add(newPlayer)

    # dummy function that send movement to the GameServer.
    def move(self, movement: Movement) -> None:
        # TO-DO: No calculation should be here! Only sends movement to via Socket
        direction, angle = movement
        player = self.l_players[0]
        angle = player.deg + DEGREE * angle
        if angle < 0:
            angle += 360
        elif angle > 360:
            angle -= 360
        dx, dy = (SPEED * cos(radians(angle)), SPEED * sin(radians(angle)))
        self.LatestSnapshot = [
            (player.rect.x + dx * direction, player.rect.y - dy * direction, angle)
        ]
