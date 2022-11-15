"""defines classes related to player"""
from abc import ABC, abstractmethod
from typing import List, Sequence, Tuple

from pygame import Vector2
import pygame as pg
from src.entity.abstract_entity import Entity
from src.helper.group import Group


class SkillParticle(Entity):
    """base class for particle of skill"""


class Skill(ABC):
    """base class for skill"""
    particle_group: Group[SkillParticle]

    @abstractmethod
    def make_particle(self, direction: Vector2) -> None:
        """attacks. make a particle, whose direction is given by the parameter"""


class Player(Entity):
    """class for player"""
    __slots__ = ("xp", "level", "money", "skills")
    xp: int
    level: int
    money: int
    skills: List[Skill]

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int]) -> None:
        super().update(key_pressed, mouse_pos)
        self.handle_key_input(key_pressed)
        print(self.transform.pos)

    def handle_key_input(self, key_pressed: Sequence[bool]):
        horizontal = -key_pressed[pg.K_a]+key_pressed[pg.K_d]
        vertical = key_pressed[pg.K_s]-key_pressed[pg.K_w]
        self.transform.direction = Vector2(horizontal, vertical)
