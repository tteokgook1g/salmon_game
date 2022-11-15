from typing import Tuple
from pygame import Rect, Surface
from pyparsing import Sequence
from src.entity.abstract_entity import Entity, Transform

class Enemy(Entity):
    """base class for enemies"""
    __slots__ = ("damage")
    damage = float

    def __init__(self, img: Surface, health: float, power: float, transform: Transform, damage) -> None:
        super().__init__(img, health, power, transform)
        self.damage = damage