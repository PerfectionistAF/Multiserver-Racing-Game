import pygame as pg
from pygame_gui import UIManager, elements, UI_BUTTON_PRESSED, UI_TEXT_ENTRY_FINISHED
from GameServerProxy import Game
from Protocols import *

def main():
#////////// Initialize pygame //////////#
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    clock = pg.time.Clock()
#////////// Initialize pygame_gui //////////#
    ui = UIManager(WINDOW_SIZE)
    chat_text_box = elements.UITextBox(relative_rect=pg.Rect((GAME_SIZE[0], GAME_SIZE[1]-CTB_HIGHT-ETB_HIGHT-BTN_HIGHT), (UI_SIZE, CTB_HIGHT)),
                                                html_text="Welcome ASU 2D Car Racer 2023",
                                                manager=ui)
    entry_text_box = elements.UITextEntryLine(relative_rect=pg.Rect((GAME_SIZE[0], GAME_SIZE[1]-BTN_HIGHT-ETB_HIGHT), (UI_SIZE, ETB_HIGHT)),
                                                placeholder_text="Chat with Friends!",
                                                manager=ui)
    send_button = elements.UIButton(relative_rect=pg.Rect((GAME_SIZE[0], GAME_SIZE[1]-BTN_HIGHT), (UI_SIZE, BTN_HIGHT)),
                                                text='send msg',
                                                manager=ui)
#////////// Initialize Game //////////#
    game = Game()
#//////////     GameLoop   //////////#
    running = True
    movement:Movement = [0, 0] # Direction and Angle
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pg.event.get(): # collapse for better readability
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
                if event.key == pg.K_UP or event.key == pg.K_w or event.key == pg.K_DOWN or event.key == pg.K_s:
                    movement[0] = 0
                if event.key == pg.K_LEFT or event.key == pg.K_d or event.key == pg.K_RIGHT or event.key == pg.K_a:
                    movement[1] = 0
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == send_button:
                    text = entry_text_box.get_text()
                    entry_text_box.set_text("")
                    chat_text_box.append_html_text(text+'\n')
            if event.type == UI_TEXT_ENTRY_FINISHED:
                text = entry_text_box.get_text()
                entry_text_box.set_text("")
                chat_text_box.append_html_text(text+'\n')
            ui.process_events(event)
        game.update(screen, movement)
        ui.update(time_delta)
        ui.draw_ui(screen)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main()