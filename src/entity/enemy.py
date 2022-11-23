from __future__ import annotations

from typing import TYPE_CHECKING, List
from pygame.math import Vector2
from src.entity.abstract_entity import Entity, PlayerCollidable, Reward
from src.entity.health_bar import HealthBar
import pygame as pg
from abc import ABC, abstractmethod
from constants import *

if TYPE_CHECKING:
    from pygame.surface import Surface

    from src.entity.abstract_entity import Transform
    from src.entity.player import Player
    from src.helper.group import Group
    from src.helper.update_info import UpdateInfo


class Enemy(Entity, PlayerCollidable):
    """base class for enemies"""
    reward_group: Group[Reward]  # ref
    skills: List[BossSkill]

    def __init__(self, img: Surface, health: float, power: float, transform: Transform) -> None:
        super().__init__(img, health, power, transform)
        self.hpbar = HealthBar(self)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if info.player is not None:
            self.transform.direction = info.player.transform.pos - self.transform.pos
        self.hpbar.update()

    def draw(self, screen: Surface):
        super().draw(screen)
        self.hpbar.draw(screen)

    def handle_collide(self, player: Player):
        super().handle_collide(player)
        player.health -= self.power
        self.transform.velocity *= -10
        self.transform.move()
        self.transform.velocity /= -10

    def kill(self) -> None:
        super().kill()
        self.reward_group.add(Reward(1, 1, self.transform.pos.copy()))


class Boss(Enemy):
    def __init__(self, img: Surface, health: float, power: float, transform: Transform) -> None:
        super().__init__(img, health, power, transform)
        self.hpbar = HealthBar(self)
        self.gun = 100
        # self.skill = BossSkill()

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        self.hpbar.update()

    def draw(self, screen: Surface):
        super().draw(screen)

    def handle_collide(self, player: Player):
        super().handle_collide(player)
        player.health -= self.power
        self.transform.velocity *= -10
        self.transform.move()
        self.transform.velocity /= -10

    def handle_collide_boss(self, player: Player):
        super().handle_collide(player)
        player.health -= self.power
        self.transform.velocity *= -10
        self.transform.move()
        self.transform.velocity /= -10

    def kill(self) -> None:
        super().kill()


class BossSkill(ABC):
    """base class for skill"""
    particle_group: Group[BossSkillParticle]

    @abstractmethod
    def make_particle(self, direction: Vector2) -> None:
        """attacks. make a particle, whose direction is given by the parameter"""


class BossSkillParticle(Entity, PlayerCollidable):
    """base class for particle of skill"""

    def __init__(self, img: Surface, health: int, power: float, transform: Transform, boss: Boss) -> None:
        super().__init__(img, health, power, transform)
        pg.sprite.Sprite.__init__(self)
        self.boss = boss
        self.transform.pos = pg.Vector2(boss.transform.pos.xy)
        self.transform.direction = pg.Vector2(
            pg.mouse.get_pos())-pg.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)/2

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if not WORLD_RECT.collidepoint(self.transform.pos.x, self.transform.pos.y):
            self.kill()

    def isinbox(self):
        return True

    def handle_collide(self, player: Player):
        player.health -= self.power
        self.kill()
