from __future__ import annotations

from typing import TYPE_CHECKING

from src.entity.abstract_entity import Entity, PlayerCollidable, Reward
from src.entity.health_bar import HealthBar

if TYPE_CHECKING:
    from pygame.surface import Surface

    from src.entity.abstract_entity import Transform
    from src.entity.player import Player
    from src.helper.group import Group
    from src.helper.update_info import UpdateInfo


class Enemy(Entity, PlayerCollidable):
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

    def handle_collide(self, player: Player):
        super().handle_collide(player)
        player.health -= self.power
        self.transform.velocity *= -10
        self.transform.move()
        self.transform.velocity /= -10

    def kill(self) -> None:
        super().kill()
        self.reward_group.add(Reward(1, 1, self.transform.pos.copy()))
