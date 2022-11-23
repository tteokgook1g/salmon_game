from typing import List
import pygame
from pygame.surface import Surface
from constants import BLACK
from src.helper.functions import render_text
from src.entity.player import Player
from src.helper.update_info import UpdateInfo
from pygame.math import Vector2

from src.entity.shop.shop_item import HealthPotion, ShopItem, SpeedPotion, PowerPotion, ShootSpeedPotion


class Shop():
    def __init__(self, player: Player):
        super().__init__()
        self.items: List[ShopItem] = []
        self.player = player

        self.items.append(HealthPotion(
            pygame.image.load("image/potion 1.png"), 10, 1))
        self.items.append(SpeedPotion(
            pygame.image.load("image/potion 2.png"), 1.025, 1))
        self.items.append(PowerPotion(
            pygame.image.load("image/potion 3.png"), 1, 1))
        self.items.append(ShootSpeedPotion(
            pygame.image.load("image/potion 4.png"), 0.975, 1))

        HealthPotion.player = player
        SpeedPotion.player = player
        PowerPotion.player = player
        ShootSpeedPotion.player = player

        for i, item in enumerate(self.items):
            item.transform.pos = Vector2(100+i*70, 300)

    def draw(self, screen: Surface):
        for item in self.items:
            item.draw(screen)
        screen.blit(render_text(
            f"$ {self.player.money}", BLACK, 40), (50, 200))

    def update(self, info: UpdateInfo):
        for item in self.items:
            item.update(info)
