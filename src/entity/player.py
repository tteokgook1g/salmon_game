"""defines classes related to player"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Sequence, Tuple

import pygame as pg
from pygame.surface import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from constants import WORLD_RECT, SCREEN_WIDTH, SCREEN_HEIGHT
import schedule  # type: ignore
from math import pi


from src.entity.health_bar import HealthBar
from src.entity.abstract_entity import Entity, Transform

if TYPE_CHECKING:
    from entity.enemy import Enemy
    from src.helper.group import Group
    from src.helper.update_info import UpdateInfo


class SkillParticle(Entity, ABC):
    def __init__(self, img: Surface, power: float, transform: Transform) -> None:
        super().__init__(img, 1, power, transform)
        schedule.every(10).seconds.do(self._kill)  # type: ignore

    def _kill(self):
        super().kill()
        return schedule.CancelJob

    def check_collide(self, enemy: Enemy) -> bool:
        return pg.sprite.collide_rect(self, enemy)

    @abstractmethod
    def handle_collide(self, enemy: Enemy):
        """handle collision with enemy"""


class GunParticle(SkillParticle):
    def __init__(self, img: Surface, power: float, velocity: float, player: Player) -> None:
        super().__init__(img,  power, Transform(
            velocity, pg.Vector2(player.transform.pos.xy), pg.Vector2(
                pg.mouse.get_pos())-pg.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)/2
        ))
        self.player = player

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if not WORLD_RECT.collidepoint(self.transform.pos.x, self.transform.pos.y):
            self.kill()

    def isinbox(self):
        return True

    def handle_collide(self, enemy: Enemy):
        enemy.health -= self.power
        self.kill()


class BombParticle(SkillParticle):
    distance = 75

    def __init__(self, img: Surface,  power: float, velocity: float, player: Player) -> None:
        transform = Transform(
            self.distance, pg.Vector2(player.transform.pos.xy), pg.Vector2(
                pg.mouse.get_pos())-pg.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)/2
        )
        transform.move()
        transform.velocity = velocity

        super().__init__(img, power, transform)
        self.player = player
        schedule.every(0.5).seconds.do(self._kill)  # type: ignore

    def _kill(self):
        super().kill()
        return schedule.CancelJob

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if not WORLD_RECT.collidepoint(self.transform.pos.x, self.transform.pos.y):
            self.kill()

    def isinbox(self):
        return True

    def handle_collide(self, enemy: Enemy):
        enemy.health -= self.power


class LightningParticle(SkillParticle):
    length_range = 100
    angle_range = 40  # -angle_range to +angle_range
    lifetime = 0.5

    def __init__(self, img: Surface, power: float, player: Player) -> None:
        self.transform = Transform(
            0, pg.Vector2(player.transform.pos.xy), pg.Vector2(
                pg.mouse.get_pos())-pg.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)/2
        )
        self.light_img = img
        self.view_radius = self.length_range//10

        lightning_img, self.rect = self.get_arc()
        img_rect = self.light_img.get_rect()
        img_rect.center = self.rect.center
        lightning_img.blit(self.light_img, img_rect)

        super().__init__(lightning_img, power, self.transform)
        self.player = player
        schedule.every(self.lifetime).seconds.do(self._kill)  # type: ignore

    def get_arc(self):
        lightning_img = Surface(
            (2*self.length_range, 2*self.length_range), pg.SRCALPHA)
        lightning_img.fill((255, 255, 255, 0))
        rect = lightning_img.get_rect()
        dir_angle = self.transform.direction.as_polar()[1] % 360

        arc_rect = Rect((0, 0, 2*self.view_radius, 2*self.view_radius))
        arc_rect.center = rect.center

        pg.draw.arc(lightning_img, (255, 255, 150),
                    arc_rect, (-self.angle_range-dir_angle)*pi/180, (self.angle_range-dir_angle)*pi/180, self.length_range//10)

        return lightning_img, rect  # type: ignore

    def _kill(self):
        super().kill()
        return schedule.CancelJob

    def update(self, info: UpdateInfo) -> None:
        self.view_radius += self.length_range*9//10/(self.lifetime*60)
        self.image, self.rect = self.get_arc()
        super().update(info)
        if not WORLD_RECT.collidepoint(self.transform.pos.x, self.transform.pos.y):
            self.kill()

    def isinbox(self):
        return True

    def check_collide(self, enemy: Enemy) -> bool:
        displacement = enemy.transform.pos-self.transform.pos
        angle = displacement.angle_to(self.transform.direction) % 360
        if displacement.length() <= self.length_range \
                and (0 <= angle <= self.angle_range or 360-self.angle_range <= angle < 360):
            return True
        return False

    def handle_collide(self, enemy: Enemy):
        enemy.health -= self.power


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

    def __init__(self, bullet_power: float):
        super().__init__()
        self.power = bullet_power
        self._speed = 10

    def _make_particle(self):
        self.particle_group.add(GunParticle(
            self.bullet_img, self.power, 5, self.player
        ))

    def bind(self, particle_group: Group[SkillParticle], player: Player):
        super().bind(particle_group, player)
        self._speed = self.player.shootspeed
        self.job = schedule.every(
            self.player.shootspeed/60).seconds.do(self._make_particle)  # type: ignore

    def update(self, info: UpdateInfo) -> None:
        if self._speed != self.player.shootspeed:
            self._speed = self.player.shootspeed
            schedule.cancel_job(self.job)
            self.job = schedule.every(
                self.player.shootspeed/60).seconds.do(self._make_particle)  # type: ignore


class BombSkill(Skill):
    __slots__ = ("power",  "cooltime")
    bomb_img = pg.image.load("image/bomb.png")
    skill_key = pg.K_e

    def __init__(self, bullet_power: float):
        super().__init__()
        self.power = bullet_power
        self.cooltime: int = 0

    def _make_particle(self):
        self.particle_group.add(BombParticle(
            self.bomb_img,  self.power, 0, self.player
        ))

    def bind(self, particle_group: Group[SkillParticle], player: Player):
        super().bind(particle_group, player)

    def update(self, info: UpdateInfo) -> None:
        self.cooltime -= 1
        if self.cooltime <= 0 and info.key_pressed[self.skill_key]:
            self._make_particle()
            self.cooltime = int(self.player.shootspeed)


class LightningSkill(Skill):
    __slots__ = ("power", "cooltime")
    lightning_img = pg.image.load("image/lightning.png")
    skill_key = pg.K_f

    def __init__(self, bullet_power: float):
        super().__init__()
        self.power = bullet_power
        self.cooltime: int = 0

    def _make_particle(self):
        self.particle_group.add(LightningParticle(
            self.lightning_img, self.power, self.player
        ))

    def bind(self, particle_group: Group[SkillParticle], player: Player):
        super().bind(particle_group, player)

    def update(self, info: UpdateInfo) -> None:
        self.cooltime -= 1
        if self.cooltime <= 0 and info.key_pressed[self.skill_key]:
            self._make_particle()
            self.cooltime = int(self.player.shootspeed)


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
        self.shootspeed: float = 60

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        self.handle_key_input(info.key_pressed)
        for skill in self.skills:
            skill.update(info)
        self.hpbar.update()

    def draw(self, screen: Surface):
        super().draw(screen)
        self.hpbar.draw(screen)

    def handle_key_input(self, key_pressed: Sequence[bool]):
        horizontal = (-key_pressed[pg.K_a]+key_pressed[pg.K_d])
        vertical = (key_pressed[pg.K_s]-key_pressed[pg.K_w])
        self.transform.direction = Vector2(horizontal, vertical)
