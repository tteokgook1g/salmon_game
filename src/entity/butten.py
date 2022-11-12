

from ast import Tuple
from pygame import Rect, Surface
from pyparsing import Sequence

from entity.abstract_entity import Transform


class Butten(Entity):
    __slots__ = ("health", "power", "transform",'string','color')
    health: float
    power: float
    transform: Transform
    rect: Rect

    def __init__(self, img: Surface, health: 0, power: 0, transform: Transform, action) -> None:
        super().__init__(img, health, power, transform)
        self.color =color
        self.stirng = string
        self.action = action 

    def click(self):
        return (self.rect.centerx-self.rect.w/2<self.mouse_pos[0]<self.rect.centerx+self.rect.w/2) and (self.rect.centery-self.rect.h/2<self.mouse_pos[1]<self.rect.centery+self.rect.h/2)

    def update(  # type: ignore
        self,
        key_pressed: Sequence[bool],
        mouse_pos: Tuple[int, int]
    ) -> None:
        """update the entity. you can use key and mouse if you need. """
        self.key_pressed = key_pressed
        self.mouse_pos = mouse_pos
        if self.mouse_pos[0] and self.click():
            self.action()
            
        self.transform.move()
        self.rect.center = int(self.transform.pos.x), int(self.transform.pos.y)

        if self.health < 0:
            self.kill()
