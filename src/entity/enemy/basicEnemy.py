import pygame as pg
from pygame.surface import Surface
from src.helper.group import Group
from src.entity.player import SkillParticle
from src.entity.health_bar import HealthBar
from src.helper.update_info import UpdateInfo
from src.entity.abstract_entity import Entity, Reward, Transform


class Enemy(Entity):
    """base class for enemies"""
    __slots__ = ("hpbar",)
    reward_group: Group[Reward]  # ref

    def __init__(self, img: Surface, health: float, power: float, transform: Transform) -> None:
        super().__init__(img, health, power, transform)
        self.hpbar = HealthBar(self)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        self.transform.direction = info.player.transform.pos - self.transform.pos
        self.hpbar.update()

    def draw(self, screen: Surface):
        super().draw(screen)
        self.hpbar.draw(screen)

    def handle_collide(self, particle: SkillParticle):
        self.health -= particle.power

    def kill(self) -> None:
        super().kill()
        self.reward_group.add(Reward(1, 1, self.transform.pos.copy()))
