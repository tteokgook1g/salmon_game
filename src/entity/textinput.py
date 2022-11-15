from typing import Sequence, Tuple

import pygame as pg
from pygame.event import Event
from pygame.surface import Surface

from src.entity.abstract_entity import Entity, Transform

pg.init()


class InputBox(Entity):
    FONT = pg.font.Font(None, 32)
    COLOR_INACTIVE = pg.Color('lightskyblue3')
    COLOR_ACTIVE = pg.Color('dodgerblue2')

    def __init__(self, img: Surface, health: int, power: int, transform: Transform, text: str):
        super().__init__(img, health, power, transform)
        self.color: pg.Color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, events: Sequence[Event]):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key == pg.K_RETURN:
                        print(self.text)
                        self.text = ''
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = self.FONT.render(
                        self.text, True, self.color)

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click: Tuple[int, int, int], events: Sequence[Event]) -> None:
        # Resize the box if the text is too long.
        self.handle_event(events)
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen: Surface):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
