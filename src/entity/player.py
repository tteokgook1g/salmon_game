"""defines classes related to player"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Sequence, Tuple, TYPE_CHECKING

import pygame as pg
from pygame.surface import Surface
from pygame.math import Vector2

from src.entity.abstract_entity import Entity, Transform
from src.helper.group import Group
from src.helper.update_info import UpdateInfo

if TYPE_CHECKING:
    from src.entity.enemy.basicEnemy import Enemy


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

    def __init__(self, img: Surface, health: float, power: float, transform: Transform, info: Tuple[int, int, int, List[Skill]]) -> None:
        super().__init__(img, health, power, transform)
        pg.sprite.Sprite.__init__(self)
        self.xp = info[0]
        self.level = info[1]
        self.money = info[2]
        self.skills = info[3]

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        self.handle_key_input(info.key_pressed)

    def handle_key_input(self, key_pressed: Sequence[bool]):
        horizontal = (-key_pressed[pg.K_a]+key_pressed[pg.K_d])
        vertical = (key_pressed[pg.K_s]-key_pressed[pg.K_w])
        self.transform.direction = Vector2(horizontal, vertical)

    def handle_collide(self, enemy: Enemy):
        self.health -= enemy.damage
