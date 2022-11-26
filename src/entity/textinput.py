from typing import Any, Callable, Sequence, Tuple

import pygame as pg
from pygame.event import Event
from pygame.surface import Surface
from pygame.mixer import Sound

from src.entity.abstract_entity import Entity, Transform
from src.helper.update_info import UpdateInfo

pg.init()


class InputBox(Entity):

    def __init__(self, img: Surface, health: int, power: int, transform: Transform, text: str, size: int, color: Tuple[int, int, int], action: Callable[[], Any]):
        super().__init__(img, health, power, transform)
        self.color = color
        self.text = text
        self.font = pg.font.Font(None, size)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.coloractive = self.color
        self.action = action

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
                self.color = self.coloractive if self.active else self.color
            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key == pg.K_RETURN:
                        self.action()
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif len(self.text) < 50 and event.key!=pg.K_SPACE:
                        self.text += event.unicode
                    # Re-render the text.
                    if len(self.text) < 30:
                        self.txt_surface = self.font.render(
                            self.text.center(30, ' '), True, self.color)
                    else:
                        self.txt_surface = self.font.render(
                            self.text, True, self.color)

    def update(self, info: UpdateInfo) -> None:
        # Resize the box if the text is too long.
        self.handle_event(info.events)
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.rect.center = int(self.transform.pos.x), int(self.transform.pos.y)

    def draw(self, screen: Surface):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, pg.rect.Rect(
            self.rect.x-5, self.rect.y-5, self.rect.w+10, self.rect.h+10), 2)
