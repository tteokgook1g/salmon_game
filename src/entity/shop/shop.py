from typing import List
import pygame
from pygame.surface import Surface
from constants import BLACK
from src.helper.functions import render_text
from src.entity.player import Player
from src.helper.update_info import UpdateInfo
from pygame.math import Vector2

from src.entity.shop.shop_item import BombItem, HealthPotion, LightningItem, ShopItem, SpeedPotion, GunPowerUpgrade, ShootSpeedPotion, MaxHealthPotion


class Shop():
    def __init__(self, player: Player):
        super().__init__()
        self.items: List[ShopItem] = []
        self.player = player

        self.items.append(HealthPotion(
            pygame.image.load("image/potion 1.png"), 10, 1))
        self.items.append(SpeedPotion(
            pygame.image.load("image/potion 2.png"), 1.02, 1))
        self.items.append(ShootSpeedPotion(
            pygame.image.load("image/potion 4.png"), 0.98, 1))
        self.items.append(MaxHealthPotion(
            pygame.image.load("image/potion 5.png"), 5, 1))
        self.items.append(GunPowerUpgrade(
            pygame.image.load("image/gun.png"), 1, 1))
        self.items.append(BombItem(
            pygame.image.load("image/bomb.png"), 0.2, 5))
        self.items.append(LightningItem(
            pygame.image.load("image/lightning.png"), 0.5, 10))

        for item in self.items:
            item.player = player

        x = 100
        for item in (self.items):
            item.transform.pos = Vector2(x, 300)
            x += item.image.get_rect().w

    def draw(self, screen: Surface):
        for item in self.items:
            item.draw(screen)
        screen.blit(render_text(
            f"$ {self.player.money}", BLACK, 40), (50, 200))

    def update(self, info: UpdateInfo):
        for item in self.items:
            item.update(info)
