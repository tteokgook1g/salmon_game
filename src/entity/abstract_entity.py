"""defines abstract classes related to Entity and implements basic functionality"""

from typing import Sequence, Tuple
from pygame import Rect
from pygame.sprite import Sprite
from pygame.math import Vector2


class Transform:
    """handle position, velocity, and direction"""
    __slots__ = ("velocity", "pos", "direction")
    velocity: float
    pos: Vector2
    direction: Vector2

    def __init__(self, velocity: float, initial_pos: Vector2, initial_direction: Vector2):
        self.velocity = velocity
        self.pos = initial_pos
        self.direction = initial_direction

    def move(self) -> None:
        """moves towards direction"""
        self.pos += self.velocity*self.direction

    def towards(self, pos: Vector2) -> None:
        """changes direction towards pos"""
        if self.pos == pos:
            return
        self.direction = (pos-self.pos).normalize()

    def away_from(self, pos: Vector2) -> None:
        """changes direction away from pos"""
        if self.pos == pos:
            return
        self.direction = -(pos-self.pos).normalize()


class Entity(Sprite):
    """base class for entities"""
    __slots__ = ("health", "power", "transform")
    health: float
    power: float
    transform: Transform
    rect: Rect

    def __init__(self, health: float, power: float, transform: Transform) -> None:
        self.health = health
        self.power = power
        self.transform = transform

    def update(  # type: ignore
        self,
        key_pressed: Sequence[bool],
        mouse_pos: Tuple[int, int]
    ) -> None:
        """update the entity. you can use key and mouse if you need. """
        self.transform.move()
        self.rect.center = int(self.transform.pos.x), int(self.transform.pos.y)

        if self.health < 0:
            self.kill()


class Enemy(Entity):
    """base class for enemies"""


class Reward(Entity):
    """rewards, which is dropped when enemies die"""
    __slots__ = ("xp", "money")
    xp: int
    money: int

    def __init__(self, xp: int, money: int):
        self.xp = xp
        self.money = money
