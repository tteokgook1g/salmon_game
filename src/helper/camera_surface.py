from typing import Tuple

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entity.abstract_entity import Transform
from src.helper.functions import lerp


class CameraSurface(Surface):
    """카메라가 있는 화면, 카메라의 위치가 화면에 중심에 위치함"""

    def __init__(self, size: Tuple[int, int], camera: Transform, flags: int = 0):
        """camera is a reference"""
        super().__init__(size=size, flags=flags | pygame.SRCALPHA)
        self.target = camera  # ref
        self.pos = camera.pos.copy()

    def update(self):
        # 카메라는 목표 위치를 천천히 따라감
        self.pos = lerp(self.pos, self.target.pos, 0.03)

    def blit(self, source: Surface, dest: Rect) -> None:  # type: ignore
        # 카메라 위치를 빼서 카메라가 중앙에 위치
        dst = dest.copy()
        dst.center = (int(dst.centerx-self.pos.x+SCREEN_WIDTH/2),
                      int(dst.centery-self.pos.y+SCREEN_HEIGHT/2))

        super().blit(source, dst)
