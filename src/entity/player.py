"""defines classes related to player"""
from abc import ABC, abstractmethod
from typing import List, Sequence, Tuple

import pygame as pg
from pygame import Vector2
from pygame.event import Event

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

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click: Tuple[int, int, int], events: Sequence[Event]) -> None:
        super().update(key_pressed, mouse_pos, mouse_click, events)
        self.handle_key_input(key_pressed)

    def handle_key_input(self, key_pressed: Sequence[bool]):
        horizontal = -key_pressed[pg.K_a]+key_pressed[pg.K_d]
        vertical = key_pressed[pg.K_s]-key_pressed[pg.K_w]
        self.transform.direction = Vector2(horizontal, vertical)
