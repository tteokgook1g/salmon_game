from typing import Any, Callable, Tuple

import pygame as pg
from pygame.rect import Rect
from pygame.surface import Surface
from src.helper.update_info import UpdateInfo

from src.entity.abstract_entity import Entity, Transform


class Button(Entity):
    __slots__ = ("power", "transform", 'string', 'color')
    rect: Rect

    def __init__(self, img: Surface, health: int, power: int, transform: Transform, action: Callable[[], Any], click_range: Tuple[int, int] | None = None) -> None:
        super().__init__(img, health, power, transform)
        self.action = action
        if click_range is None:
            self.click_rect = self.rect
        else:
            self.click_rect = Rect(0, 0, *click_range)
            self.click_rect.center = self.rect.center

    def update(  # type: ignore
        self,
        info: UpdateInfo
    ) -> None:
        """update the entity. you can use key and mouse if you need. """
        super().update(info)
        self.click_rect.center = self.rect.center
        for event in info.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.click_rect.collidepoint(event.pos):
                    self.action()
