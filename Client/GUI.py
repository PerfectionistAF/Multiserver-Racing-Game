import pygame_gui as gui
from pygame import Rect, Color

from Protocols import *


class GUI:
    def __init__(self, mailBoxIn: list[str], mailBoxOut: list[str]) -> None:
        self.playButtonPressed = False
        self.mailBoxIn = mailBoxIn
        self.mailBoxOut = mailBoxOut
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
        if self.mailBoxIn:
            self.readMail()
        self.manager.update(time_delta)
        self.manager.draw_ui(screen)

    def handelEvents(self, event) -> None:
        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button and self.playButtonPressed:
                self.sendMessage()
            else:
                self.playButtonPressed = True
        if event.type == gui.UI_TEXT_ENTRY_FINISHED and self.playButtonPressed:
            self.sendMessage()
        self.manager.process_events(event)

    def sendMessage(self):
        text = self.entry_text_box.get_text()
        self.entry_text_box.set_text('')
        self.chat_text_box.append_html_text(text + '\n')
        self.mailBoxOut.append(text)

    def readMail(self) -> None:
        for message in self.mailBoxIn:
            self.chat_text_box.append_html_text(
                f'<font color={COLORS[int(message[0])]}>{message[1:]}</font>' + '\n'
            )
        self.mailBoxIn.clear()
