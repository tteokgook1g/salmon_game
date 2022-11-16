"""defines classes related to player"""
from abc import ABC, abstractmethod
from typing import List

from pygame import Vector2, Rect, Surface
from src.entity.abstract_entity import Entity
from src.helper.group import Group
from typing import Tuple
from pyparsing import Sequence
from src.entity.abstract_entity import Entity, Transform

class health_potion(Entity):
    def __init__(self, img: Surface, health: 0, power: 0, transform: Transform, health_plus) -> None:
        self.health_plus = health_plus
        self.num = 0

    def buy(self):
        self.num += 1

    def use_potion(self):
        if self.num >= 1:
            self.health += self.health_plus
            self.num -= 1

class speed_potion(Entity):
    def __init__(self, img: Surface, health: 0, power: 0, transform: Transform, speed_plus) -> None:
        self.speed_plus = speed_plus
        self.num = 0

    def buy(self):
        self.num += 1

    def use_potion(self):
        if self.num >= 1:
            self.transform.velocity += self.speed_plus
            self.num -= 1