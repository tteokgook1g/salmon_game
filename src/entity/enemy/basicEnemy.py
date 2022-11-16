import pygame as pg
from pygame.surface import Surface

from src.helper.update_info import UpdateInfo
from src.entity.abstract_entity import Entity, Transform


class Enemy(Entity):
    """base class for enemies"""
    __slots__ = ("damage")
    damage: float

    def __init__(self, img: Surface, health: float, power: float, transform: Transform, damage: float) -> None:
        super().__init__(img, health, power, transform)
        pg.sprite.Sprite.__init__(self)
        self.damage = damage

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        self.transform.direction = info.player.transform.pos - self.transform.pos

    def iscollide(self, enemy):
        self.health -= enemy.damage
        print(self.health)
