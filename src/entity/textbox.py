from typing import Sequence, Tuple

import pygame as pg
from pygame.event import Event
from pygame.surface import Surface

from src.entity.abstract_entity import Entity, Transform

pg.init()


class TextBox(Entity):

    def __init__(self, img: Surface, health: int, power: int, transform: Transform, text: str, size:int, color: Tuple[int,int,int]):
        super().__init__(img, health, power, transform)
        self.color= color
        self.text = text
        self.font = pg.font.Font(None, size)
        self.txt_surface = self.font.render(text.center(30,' '), True, self.color)
        self.active = False
        self.coloractive = self.color

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click: Tuple[int, int, int], events: Sequence[Event]) -> None:
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.rect.center = int(self.transform.pos.x), int(self.transform.pos.y)

    def draw(self, screen: Surface):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, pg.rect.Rect(self.rect.x-5,self.rect.y-5,self.rect.w+10,self.rect.h+10),2)
