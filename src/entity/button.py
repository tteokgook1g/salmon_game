from typing import Any, Callable, Tuple
from pygame.rect import Rect
from pygame.surface import Surface
from typing import Sequence
from src.entity.abstract_entity import Entity, Transform


class Button(Entity):
    __slots__ = ("health", "power", "transform", 'string', 'color')
    health: float
    power: float
    transform: Transform
    rect: Rect

    def __init__(self, img: Surface, health: int, power: int, transform: Transform, action: Callable[[], Any]) -> None:
        super().__init__(img, health, power, transform)
        self.action = action

    def isinbox(self):
        return (self.rect.left < self.mouse_pos[0] < self.rect.right) and (self.rect.top < self.mouse_pos[1] < self.rect.bottom)

    def update(  # type: ignore
        self,
        key_pressed: Sequence[bool],
        mouse_pos: Tuple[int, int],
        mouse_click: Tuple[int, int, int]
    ) -> None:
        """update the entity. you can use key and mouse if you need. """
        Entity.update(self, key_pressed, mouse_pos, mouse_click)
        if self.mouse_click[0] and self.isinbox():
            self.action()
