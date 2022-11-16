"""defines abstract classes related to Entity and implements basic functionality"""


from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface
from constants import WORLD_BORDER
from src.helper.update_info import UpdateInfo


class Transform:
    """handle position, velocity, and direction"""
    __slots__ = ("velocity", "pos", "_dir")
    velocity: float
    pos: Vector2
    _dir: Vector2

    def __init__(self, velocity: float, initial_pos: Vector2, initial_direction: Vector2):
        self.velocity = velocity
        self.pos = initial_pos
        self._dir = initial_direction

    def move(self) -> None:
        """moves towards direction"""
        self.pos += self.velocity*self._dir

    def towards(self, pos: Vector2) -> None:
        """changes direction towards pos"""
        if self.pos == pos:
            return
        self._dir = (pos-self.pos).normalize()

    def away_from(self, pos: Vector2) -> None:
        """changes direction away from pos"""
        if self.pos == pos:
            return
        self._dir = -(pos-self.pos).normalize()

    @property
    def direction(self) -> Vector2:
        return self._dir

    @direction.setter
    def direction(self, value: Vector2) -> None:
        if value.length() == 0:
            self._dir = value
        else:
            self._dir = value.normalize()


class Entity(Sprite):
    """base class for entities"""
    __slots__ = ("health", "power", "transform")
    health: float
    power: float
    transform: Transform
    rect: Rect
    image: Surface

    def __init__(self, img: Surface, health: float, power: float, transform: Transform) -> None:
        super().__init__()
        self.image = img
        self.rect = img.get_rect()

        self.rect.center = int(transform.pos.x), int(transform.pos.y)
        self.health = health
        self.power = power
        self.transform = transform

    def update(self, info: UpdateInfo) -> None:  # type: ignore
        """update the entity. you can use key and mouse if you need. """
        self.key_pressed = info.key_pressed
        self.mouse_pos = info.mouse_pos
        self.mouse_click = info.mouse_click

        next_pos = (self.transform.pos+self.transform.direction *
                    self.transform.velocity)
        if (self.rect.size[0]/2 < next_pos.x < WORLD_BORDER-self.rect.size[0]/2 and
                self.rect.size[1]/2 < next_pos.y < WORLD_BORDER-self.rect.size[1]/2):
            self.transform.move()
        self.rect.center = int(self.transform.pos.x), int(self.transform.pos.y)

        if self.health < 0:
            self.kill()


class Reward(Entity):
    """rewards, which is dropped when enemies die"""
    __slots__ = ("xp", "money")
    xp: int
    money: int

    def __init__(self, xp: int, money: int):
        self.xp = xp
        self.money = money
