from __future__ import annotations

from typing import TYPE_CHECKING

from constants import *
from src.entity.abstract_entity import Entity, PlayerCollidable, Reward
from src.entity.health_bar import HealthBar

if TYPE_CHECKING:
    from pygame.surface import Surface

    from src.entity.abstract_entity import Transform
    from src.entity.player import Player
    from src.helper.group import Group
    from src.helper.update_info import UpdateInfo


class Enemy(Entity, PlayerCollidable):
    """class for enemies"""
    reward_group: Group[Reward]  # ref

    def __init__(self, img: Surface, health: float, power: float, transform: Transform, rewardnum: int) -> None:
        super().__init__(img, health, power, transform)
        self.hpbar = HealthBar(self)
        self.rewardnum = rewardnum

    def update(self, info: UpdateInfo) -> None:
        super().update(info)

        # 플레이어 방향을 향함
        if info.player is not None:
            self.transform.direction = info.player.transform.pos - self.transform.pos
        self.hpbar.update()

    def draw(self, screen: Surface):
        super().draw(screen)
        self.hpbar.draw(screen)

    def handle_collide(self, player: Player):
        super().handle_collide(player)
        player.health -= self.power

        # 플레이어와 충돌 시 반대 방향으로 튕겨 나감
        self.transform.velocity *= -10
        self.transform.move()
        self.transform.velocity /= -10

    def kill(self):
        # 죽으면 Reward를 떨어트림
        self.reward_group.add(
            Reward(self.rewardnum, self.rewardnum, self.transform.pos.copy()))
        return super().kill()


class Boss(Enemy):
    def __init__(self, img: Surface, health: float, power: float, transform: Transform, rewardnum: int) -> None:
        super().__init__(img, health, power, transform, rewardnum)
        self.hpbar = HealthBar(self)
        self.gun = 100

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        self.hpbar.update()

    def handle_collide(self, player: Player):
        super().handle_collide(player)
        player.health -= self.power
        self.transform.velocity *= -10
        self.transform.move()
        self.transform.velocity /= -10
