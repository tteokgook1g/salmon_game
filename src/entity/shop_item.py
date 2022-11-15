"""defines classes related to player"""
from abc import ABC, abstractmethod
from typing import List

from pygame import Vector2, Rect, Surface
from src.entity.abstract_entity import Entity
from src.helper.group import Group
from typing import Tuple
from pyparsing import Sequence
from src.entity.abstract_entity import Entity, Transform

class shop_item(Entity):
    def __init__(self, img: Surface, health: 0, power: 0, transform: Transform, passive, health_plus, vec_plus, invisible) -> None:
        super().__init__(img, health, power, transform)
        self.passive = passive
        self.health_plus = health_plus
        self.vec_plus = vec_plus
        self.invisible = invisible
