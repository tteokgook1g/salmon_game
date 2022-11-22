"""defines classes related to player"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface
from src.helper.update_info import UpdateInfo
from src.entity.button import Button
from src.entity.abstract_entity import Entity, Transform
if TYPE_CHECKING:
    from src.entity.player import Player

class ShopItem(Sprite, ABC):
    button_img: Surface = pg.image.load("image/buy_button.png")
    player: Player
    rect: Rect

    def __init__(self, img: Surface):
        super().__init__()
        self.transform = Transform(0, Vector2(0, 0), Vector2(0, 0))
        self.button = Button(self.button_img, 1, 0, self.transform, self.buy)

        temp = Surface((60, 60), pg.SRCALPHA)
        temp.fill((255, 255, 255, 255))

        img_rect = img.get_rect()
        temp.blit(img, img_rect)
        button_rect = self.button.rect.copy()
        button_rect.midtop = img_rect.centerx, img_rect.bottom+10
        temp.blit(self.button.image, button_rect)

        self.img = temp
        self.rect = self.img.get_rect()

    def draw(self, screen: Surface):
        screen.blit(self.img, self.rect)

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

class PowerPotion(ShopItem):
    def __init__(self, img: Surface, power_plus: float, price: int) -> None:
        super().__init__(img)
        self.power_plus = power_plus
        self.price = price

    def buy(self):
        if self.player.money >= self.price:
            self.player.money -= self.price
            self.player.power += self.power_plus

# class SpeedPotion(ShopItem):
#     def __init__(self, img: Surface, attackspeed_plus: float, price: int) -> None:
#         super().__init__(img)
#         self.speed_plus = attackspeed_plus
#         self.price = price

#     def buy(self):
#         if self.player.money >= self.price:
#             self.player.money -= self.price

class bomb(Entity):
    pass

class lightning(Entity):
    pass