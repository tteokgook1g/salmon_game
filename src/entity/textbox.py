from typing import Tuple

import pygame as pg
from pygame.surface import Surface

from src.helper.functions import vector_to_tuple
from src.entity.abstract_entity import Entity, Transform
from src.helper.update_info import UpdateInfo

pg.init()


class TextBox(Entity):
    """텍스트를 띄워주는 클래스"""

    def __init__(self, img: Surface, health: int, power: int, transform: Transform, text: str, size: int, color: Tuple[int, int, int]):
        super().__init__(img, health, power, transform)
        self.color = color
        self.text = text
        self.font = pg.font.Font(None, size)
        self.txt_surface = self.font.render(
            text.center(30, ' '), True, self.color)
        self.active = False
        self.coloractive = self.color

    def update(self, info: UpdateInfo) -> None:
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.rect.center = vector_to_tuple(self.transform.pos)

    def draw(self, screen: Surface):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, pg.rect.Rect(
            self.rect.x-5, self.rect.y-5, self.rect.w+10, self.rect.h+10), 2)


class TextBox2(Entity):
    """텍스트를 띄워주는 클래스"""

    def __init__(self, img: Surface, health: int, power: int, transform: Transform, text: str, size: int, color: Tuple[int, int, int]):
        super().__init__(img, health, power, transform)
        self.color = color
        self.text = text
        self.font = pg.font.Font(None, size)
        self.txt_surface = self.font.render(
            text, True, self.color)
        self.active = False
        self.coloractive = self.color

    def update(self, info: UpdateInfo) -> None:
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.rect.center = int(self.transform.pos.x), int(self.transform.pos.y)

    def draw(self, screen: Surface):
        # Blit the text.
        screen.blit(self.txt_surface, pg.rect.Rect(
            self.rect.x+5, self.rect.y+5, self.rect.w, self.rect.h))
