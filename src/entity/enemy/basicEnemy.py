from typing import Tuple
from pygame import Rect, Surface
from pyparsing import Sequence
from src.entity.abstract_entity import Entity, Transform

class Enemy(Entity):
    """base class for enemies"""