"""defines classes related to player"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame as pg
from pygame.math import Vector2
from pygame.sprite import Sprite
from pygame.surface import Surface

from src.entity.abstract_entity import Entity, Transform
from src.entity.button import Button
from src.entity.player import BombSkill, GunSkill, LightningSkill
from src.helper.update_info import UpdateInfo

if TYPE_CHECKING:
    from pygame.rect import Rect

    from src.entity.player import Player


class ShopItem(Sprite, ABC):
    button_img: Surface = pg.image.load("image/buy_button.png")
    player: Player
    rect: Rect
    image: Surface

    def __init__(self, img: Surface):
        super().__init__()
        self.transform = Transform(0, Vector2(0, 0), Vector2(0, 0))
        self.button = Button(self.button_img, 1, 0, self.transform, self.buy)

        img_rect = img.get_rect()
        button_rect = self.button.rect
        padding = 20

        temp = Surface((max(img_rect.w, button_rect.w+2*padding),
                       img_rect.h+button_rect.h+3*padding), pg.SRCALPHA)
        temp.fill((255, 255, 255, 200))
        temp_rect = temp.get_rect()
        self.button.click_rect.w, self.button.click_rect.h = temp_rect.w, temp_rect.h

        img_rect.center = temp_rect.centerx, temp_rect.top+2*padding
        temp.blit(img, img_rect)

        button_rect.midtop = temp_rect.centerx+padding, img_rect.bottom+padding
        temp.blit(self.button.image, button_rect)

        self.image = temp
        self.rect = self.image.get_rect()

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)

    def update(self, info: UpdateInfo):  # type: ignore
        self.rect.center = int(self.transform.pos.x), int(self.transform.pos.y)
        self.button.update(info)

    @abstractmethod
    def buy(self):
        """handles when buy button is clicked"""


class HealthPotion(ShopItem):
    def __init__(self, img: Surface, health_plus: int, price: int) -> None:
        super().__init__(img)
        self.health_plus = health_plus
        self.price = price

    def buy(self):
        if self.player.money >= self.price:
            self.player.money -= self.price
            self.player.health += self.health_plus


class SpeedPotion(ShopItem):
    def __init__(self, img: Surface, speed_plus: float, price: int) -> None:
        super().__init__(img)
        self.speed_plus = speed_plus
        self.price = price

    def buy(self):
        if self.player.money >= self.price:
            self.player.money -= self.price
            self.player.transform.velocity += self.speed_plus


class GunPowerUpgrade(ShopItem):
    def __init__(self, img: Surface, power_plus: float, price: int) -> None:
        super().__init__(img)
        self.power_plus = power_plus
        self.price = price
        self.gun: GunSkill | None = None

    def buy(self):
        try:
            self.gun = self.player.skills["gun"]  # type: ignore
        except KeyError:
            pass

        if self.player.money >= self.price:
            self.player.money -= self.price
            if self.gun is None:
                gun_skill = GunSkill(10)
                self.player.skills["gun"] = gun_skill
                gun_skill.bind(self.player.skill_particles, self.player)
                self.gun = gun_skill
            else:
                self.gun.power += self.power_plus


class ShootSpeedPotion(ShopItem):
    def __init__(self, img: Surface, shootspeed_decrese: float, price: int) -> None:
        super().__init__(img)
        self.shootspeed_decrease = shootspeed_decrese
        self.price = price

    def buy(self):
        if self.player.money >= self.price:
            self.player.money -= self.price
            self.player.shootspeed *= self.shootspeed_decrease


class MaxHealthPotion(ShopItem):
    def __init__(self, img: Surface, max_health_plus: float, price: int) -> None:
        super().__init__(img)
        self.max_health_plus = max_health_plus
        self.price = price

    def buy(self):
        if self.player.money >= self.price:
            self.player.money -= self.price
            self.player.fullhp += self.max_health_plus


class BombItem(ShopItem):
    def __init__(self, img: Surface, power_plus: float, price: int) -> None:
        super().__init__(img)
        self.power_plus = power_plus
        self.price = price
        self.bomb: BombSkill | None = None

    def buy(self):
        try:
            self.bomb = self.player.skills["bomb"]  # type: ignore
        except KeyError:
            pass

        if self.player.money >= self.price:
            self.player.money -= self.price
            if self.bomb is None:
                bomb_skill = BombSkill(2)
                self.player.skills["bomb"] = bomb_skill
                bomb_skill.bind(self.player.skill_particles, self.player)
                self.bomb = bomb_skill
            else:
                self.bomb.power += self.power_plus


class LightningItem(ShopItem):
    def __init__(self, img: Surface, power_plus: float, price: int) -> None:
        super().__init__(img)
        self.power_plus = power_plus
        self.price = price
        self.lightning: LightningSkill | None = None

    def buy(self):
        try:
            self.lightning = self.player.skills["lightning"]  # type: ignore
        except KeyError:
            pass

        if self.player.money >= self.price:
            self.player.money -= self.price
            if self.lightning is None:
                lightning_skill = LightningSkill(5)
                self.player.skills["lightning"] = lightning_skill
                lightning_skill.bind(self.player.skill_particles, self.player)
                self.lightning = lightning_skill
            else:
                self.lightning.power += self.power_plus


class lightning(Entity):
    pass
