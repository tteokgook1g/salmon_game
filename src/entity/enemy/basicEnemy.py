import pygame as pg
from pygame.surface import Surface
from src.entity.player import Player

from src.helper.update_info import UpdateInfo
from src.entity.abstract_entity import Entity, Transform


class Enemy(Entity):
    """base class for enemies"""
    __slots__ = ()


    def __init__(self, img: Surface, health: float, power: float, transform: Transform) -> None:
        super().__init__(img, health, power, transform)
        pg.sprite.Sprite.__init__(self)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        self.transform.direction = info.player.transform.pos - self.transform.pos

