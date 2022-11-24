from typing import Tuple

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entity.abstract_entity import Transform


class CameraSurface(Surface):
    def __init__(self, size: Tuple[int, int], camera: Transform, flags: int = 0):
        """camera is a reference"""
        super().__init__(size=size, flags=flags | pygame.SRCALPHA)
        self.target = camera  # ref
        self.pos = camera.pos.copy()
        self.ratio = 0.1

    def update(self):
        self.pos = (self.pos*(1-self.ratio)+self.target.pos*self.ratio)
        print(self.pos, self.target.pos)

    def blit(self, source: Surface, dest: Rect) -> None:  # type: ignore
        dst = dest.copy()
        dst.center = (int(dst.centerx-self.pos.x+SCREEN_WIDTH/2),
                      int(dst.centery-self.pos.y+SCREEN_HEIGHT/2))

        super().blit(source, dst)
