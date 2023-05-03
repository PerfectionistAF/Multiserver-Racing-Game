import math
from Protocols import *
from Player import Player
from pygame import sprite, Surface, image, transform

class Game(object): # Should be a singleton
    def __init__(self) -> None:
        self.State: GameState = GameState.MainMenu
        self.g_players = sprite.RenderClear()
        self.LatestSnapshot: GameSnapshot = GameSnapshot
        self.map = image.load("./Sprites/Map.png").convert()
        self.map = transform.scale(self.map, GAME_SIZE)
        self.l_players: PlayerList = {}

    #TO-DO: Receive snapshot from GameServer and update the LatestSnapshot
    def getSnapshot(self) -> None:
        self.LatestSnapshot = [(100, 100, 0)]

    def update(self, screen: Surface, movement:Movement) -> None:
        match self.State:
            case GameState.MainMenu:
                screen.blit(self.map, (0,0))
                self.State = GameState.GameSetup # TO-DO: Setup a Socket to connect to a game
            case GameState.GameSetup:
                self.getSnapshot() # starts a Thread+Socket to continuously receive the LatestSnapshot
                self.id = 0 # TO-DO: get this Game instance's id from server
                Waiting = True
                while Waiting:
                    Waiting = False # TO-DO: switch game state when the GameServer is ready
                self.__CreatePlayer(0) # TO-DO: Create x number of Players as decreed by the GameServer
                self.State = GameState.GamePlay
            case GameState.GamePlay:
                self.g_players.update(self.LatestSnapshot)
                self.g_players.clear(screen, self.map)
                self.g_players.draw(screen)
                self.move(movement)
                #TO-DO: listen to GameServer for winner and go to the next State
            case GameState.GameEnd:
                pass

    def __CreatePlayer(self, id) -> None:
        #TO-DO: get id of other players and create players
        self.l_players[id] = Player(id)
        self.g_players.add(self.l_players[id])

    # dummy function that send movement to the GameServer.
    # signature should be def move(self, movement: Movement) -> None: // it won't send id
    def move(self, movement: Movement, id=0) -> None:
        # TO-DO: No calculation should be here! Only sends movement to via Socket
        direction, angle = movement
        p:Player = self.l_players[id]
        angle = p.deg + DEGREE*angle
        if angle < 0:
            angle += 360
        elif angle > 360:
            angle -= 360
        dx, dy = (SPEED*math.cos(math.radians(angle)),SPEED*math.sin(math.radians(angle)))
        self.LatestSnapshot = [(p.rect.x+dx*direction, p.rect.y-dy*direction, angle)]
