"""defines classes related to player"""
from abc import ABC, abstractmethod
import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2
from pygame.surface import Surface
from src.entity.button import Button
from src.entity.abstract_entity import Entity
from src.entity.abstract_entity import Entity, Transform


class ShopItem(Sprite, ABC):
    button_img: Surface = pg.image.load("image/buy_button.png")

    def __init__(self, img: Surface):
        super().__init__()
        self.img = img
        self.rect = img.get_rect()
        self.button = Button(self.button_img, 1, 0, Transform(
            0, Vector2(0, 0), Vector2(0, 0)), self.buy)

    @abstractmethod
    def buy(self):
        """handles when buy button is clicked"""


class HealthPotion(Entity):
    def __init__(self, img: Surface, health: 0, power: 0, transform: Transform, health_plus) -> None:
        self.health_plus = health_plus
        self.num = 0

    def buy(self):
        self.num += 1

    def use_potion(self):
        if self.num >= 1:
            self.health += self.health_plus
            self.num -= 1


class speed_potion(Entity):
    def __init__(self, img: Surface, health: 0, power: 0, transform: Transform, speed_plus) -> None:
        self.speed_plus = speed_plus
        self.num = 0

    def buy(self):
        self.num += 1

    def use_potion(self):
        if self.num >= 1:
            self.transform.velocity += self.speed_plus
            self.num -= 1


class bomb(Entity):
    pass


class lightning(Entity):
    pass
