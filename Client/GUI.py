import pygame_gui as gui
from pygame import Rect

from Protocols import *


class GUI:
    def __init__(self) -> None:
        self.playButtonPressed = False
        self.manager = gui.UIManager(WINDOW_SIZE)
        self.chat_text_box = gui.elements.UITextBox(
            relative_rect=Rect(
                GAME_SIZE[0],
                GAME_SIZE[1] - CTB_HIGHT - ETB_HIGHT - BTN_HIGHT,
                UI_SIZE,
                CTB_HIGHT,
            ),
            html_text='Welcome ASU 2D Car Racer 2023',
            manager=self.manager,
        )
        self.entry_text_box = gui.elements.UITextEntryLine(
            relative_rect=Rect(
                GAME_SIZE[0], GAME_SIZE[1] - BTN_HIGHT - ETB_HIGHT, UI_SIZE, ETB_HIGHT
            ),
            placeholder_text='Chat with Friends!',
            manager=self.manager,
        )
        self.button = gui.elements.UIButton(
            relative_rect=Rect(
                GAME_SIZE[0], GAME_SIZE[1] - BTN_HIGHT, UI_SIZE, BTN_HIGHT
            ),
            text='',
            manager=self.manager,
        )

    def update(self, screen, time_delta):
        self.button.set_text('send msg' if self.playButtonPressed else 'Find Game')
        self.manager.update(time_delta)
        self.manager.draw_ui(screen)

    def handelEvents(self, event) -> None:
        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button and self.playButtonPressed:
                text = self.entry_text_box.get_text()
                self.entry_text_box.set_text('')
                self.chat_text_box.append_html_text(text + '\n')
            else:
                self.playButtonPressed = True
        if event.type == gui.UI_TEXT_ENTRY_FINISHED and self.playButtonPressed:
            text = self.entry_text_box.get_text()
            self.entry_text_box.set_text('')
            self.chat_text_box.append_html_text(text + '\n')
        self.manager.process_events(event)

    def checkMailBox(self, messages: list[str]) -> None:
        for message in messages:
            self.chat_text_box.append_html_text(message + '\n')
        messages.clear()
