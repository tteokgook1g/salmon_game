"""defines classes related to player"""
from abc import ABC, abstractmethod
from typing import List

from pygame import Vector2
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
