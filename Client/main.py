import atexit
import pygame as pg

from GameProxy import Game
from Protocols import *


def main():
    global game
    running = True
    movement: Movement = [0, 0]
    while running:
        for event in pg.event.get():  # collapse for better readability
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    movement[0] = 1
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    movement[0] = -1
                if event.key == pg.K_LEFT or event.key == pg.K_d:
                    movement[1] = 1
                if event.key == pg.K_RIGHT or event.key == pg.K_a:
                    movement[1] = -1
            if event.type == pg.KEYUP:
                if (
                    event.key == pg.K_UP
                    or event.key == pg.K_w
                    or event.key == pg.K_DOWN
                    or event.key == pg.K_s
                ):
                    movement[0] = 0
                if (
                    event.key == pg.K_LEFT
                    or event.key == pg.K_d
                    or event.key == pg.K_RIGHT
                    or event.key == pg.K_a
                ):
                    movement[1] = 0
            game.UI.handelEvents(event)
        game.update(movement)
    game.quit()


def exit_handler():
    global game
    if game.initialized:
        print("game closed abruptly")
        game.quit()


if __name__ == "__main__":
    atexit.register(exit_handler)
    game = Game()
    main()
