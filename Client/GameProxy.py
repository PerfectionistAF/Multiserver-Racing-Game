import pygame as pg

from GUI import GUI
from Proxy import Proxy
from Player import Player
from Protocols import *


class Game:
    def __init__(self) -> None:
        self._initGame()
        self.mailBoxIn = []
        self.mailBoxOut = []
        self.UI = GUI(self.mailBoxIn, self.mailBoxOut)
        self.proxy = Proxy(self.mailBoxIn, self.mailBoxOut)

    def update(self, movement: Movement) -> None:
        time_delta = self.clock.tick(60) / 1000.0
        match self.proxy.state:
            case GameState.MainMenu:
                self.screen.blit(self.map, (0, 0))
                if self.UI.playButtonPressed:
                    self.proxy.start()
                    self.proxy.state = GameState.GameSetup
            case GameState.GameSetup:
                if self.proxy.playerCount is not None:
                    for id in range(self.proxy.playerCount):
                        newPlayer = Player(id)
                        self.g_players.add(newPlayer)
                    self.proxy.state = GameState.GamePlay
            case GameState.GamePlay:
                self.g_players.update(self.proxy.LatestSnapshot)
                self.g_players.clear(self.screen, self.map)
                self.g_players.draw(self.screen)
                self.proxy.move(movement)
            case GameState.GameEnd:
                self.UI.playButtonPressed = False
                self.g_players.empty()
                self.proxy.close()
                self.proxy = Proxy(self.mailBoxIn, self.mailBoxOut)
        self.UI.update(self.screen, time_delta)
        pg.display.update()

    def quit(self) -> None:
        self.proxy.close()
        if self.proxy.ident:
            self.proxy.join()
        pg.quit()

    def _initGame(self):
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.g_players = pg.sprite.RenderClear()
        self.map = pg.image.load('./Sprites/Map.png').convert()
        self.map = pg.transform.scale(self.map, GAME_SIZE)
