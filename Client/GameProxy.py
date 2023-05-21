from pygame import sprite, Surface, image, transform

from Proxy import Proxy
from Player import Player
from Protocols import GAME_SIZE, Movement, GameState


class Game:
    def __init__(self, addr=None) -> None:
        self.g_players = sprite.RenderClear()
        self.map = image.load("./Sprites/Map.png").convert()
        self.map = transform.scale(self.map, GAME_SIZE)
        self.state: GameState = GameState.MainMenu
        self.proxy = Proxy(addr)

    def addPlayer(self, id) -> None:
        newPlayer = Player(id)
        self.g_players.add(newPlayer)

    def update(self, screen: Surface, movement: Movement) -> None:
        match self.state:
            case GameState.MainMenu:
                screen.blit(self.map, (0, 0))
                if self.proxy.waitOtherPlayers():
                    self.state = GameState.GameSetup
            case GameState.GameSetup:
                for i in range(len(self.proxy.LatestSnapshot)):
                    self.addPlayer(i)
                self.proxy.start()
                self.state = GameState.GamePlay
            case GameState.GamePlay:
                self.g_players.update(self.proxy.LatestSnapshot)
                self.g_players.clear(screen, self.map)
                self.g_players.draw(screen)
                self.proxy.move(movement)
                if not self.proxy.is_alive():
                    self.g_players.empty()
                    self.state = GameState.GameEnd
            case GameState.GameEnd:
                self.proxy = Proxy()
                self.state = GameState.MainMenu
