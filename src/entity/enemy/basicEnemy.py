import pygame as pg
from pygame.event import Event
from typing import Tuple
from pygame import Rect, Surface, Vector2
from pyparsing import Sequence
from src.entity.player import Player
from src.entity.abstract_entity import Entity, Transform

class Enemy(Entity):
    """base class for enemies"""
    __slots__ = ("damage")
    damage : float

    def __init__(self, img: Surface, health: float, power: float, transform: Transform, damage: float) -> None:
        super().__init__(img, health, power, transform)
        pg.sprite.Sprite.__init__(self)
        self.damage = damage

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click: Tuple[int, int, int], events: Sequence[Event],player : Player) -> None:
        super().update(key_pressed, mouse_pos, mouse_click, events)
        self.transform.direction = player.transform.pos - self.transform.pos

    def iscollide(self,enemy):
        self.health -= enemy.damage
        print(self.health)