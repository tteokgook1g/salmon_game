"""defines classes related to player"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Sequence, Tuple

import pygame as pg
from pygame.surface import Surface
from pygame.math import Vector2
from constants import WORLD_RECT, SCREEN_WIDTH, SCREEN_HEIGHT
import schedule  # type: ignore


from src.entity.health_bar import HealthBar
from src.entity.abstract_entity import Entity, Transform

if TYPE_CHECKING:
    from entity.enemy import Enemy
    from src.helper.group import Group
    from src.helper.update_info import UpdateInfo


class SkillParticle(Entity, ABC):
    @abstractmethod
    def handle_collide(self, enemy: Enemy):
        """handle collision with enemy"""


class GunParticle(SkillParticle):
    """base class for particle of skill"""

    def __init__(self, img: Surface, health: int, power: float, transform: Transform, player: Player) -> None:
        super().__init__(img, health, power, transform)
        self.player = player
        self.transform.pos = pg.Vector2(player.transform.pos.xy)
        self.transform.direction = pg.Vector2(
            pg.mouse.get_pos())-pg.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)/2

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if not WORLD_RECT.collidepoint(self.transform.pos.x, self.transform.pos.y):
            self.kill()

    def isinbox(self):
        return True

    def handle_collide(self, enemy: Enemy):
        enemy.health -= self.power
        self.kill()


class Skill(ABC):
    """base class for skill"""
    __slots__ = ("particle_group", "player")

    @abstractmethod
    def update(self, info: UpdateInfo) -> None:
        """check info and attacks if condition matches."""

    def bind(self, particle_group: Group[SkillParticle], player: Player):
        """binds particle_group and player. must call before use"""
        self.particle_group: Group[SkillParticle] = particle_group
        self.player: Player = player


class GunSkill(Skill):
    __slots__ = ("power", "_speed", "job")
    bullet_img = Surface((10, 10))
    bullet_img.fill((255, 0, 0))

    def __init__(self, bullet_power: float, attack_speed: float):
        super().__init__()
        self.power = bullet_power
        self._speed = attack_speed

    def _make_particle(self):
        self.particle_group.add(GunParticle(
            self.bullet_img, 3, self.power, Transform(5, Vector2(
                self.player.transform.pos.xy), Vector2(1, 0)), self.player
        ))

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value: float):
        self._speed = value
        schedule.cancel_job(self.job)
        self.job = schedule.every(
            1/self.speed).seconds.do(self._make_particle)  # type: ignore

    def bind(self, particle_group: Group[SkillParticle], player: Player):
        super().bind(particle_group, player)
        self.job = schedule.every(
            1/self.speed).seconds.do(self._make_particle)  # type: ignore

    def update(self, info: UpdateInfo) -> None:
        pass


class Player(Entity):
    """class for player"""
    __slots__ = ("xp", "level", "money", "skills")

    def __init__(self, img: Surface, health: float, power: float, transform: Transform, info: Tuple[int, int, int, List[Skill]]) -> None:
        """info[0] is xp, info[1] is level, info[2] is money"""
        super().__init__(img, health, power, transform)
        self.xp: int = info[0]
        self.level: int = info[1]
        self.money: int = info[2]
        self.skills: List[Skill] = info[3]
        self.hpbar = HealthBar(self)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        self.handle_key_input(info.key_pressed)
        self.hpbar.update()

    def draw(self, screen: Surface):
        super().draw(screen)
        self.hpbar.draw(screen)

    def handle_key_input(self, key_pressed: Sequence[bool]):
        horizontal = (-key_pressed[pg.K_a]+key_pressed[pg.K_d])
        vertical = (key_pressed[pg.K_s]-key_pressed[pg.K_w])
        self.transform.direction = Vector2(horizontal, vertical)
