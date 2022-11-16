from typing import Tuple
from pyparsing import Sequence
from src.entity.abstract_entity import Entity, Transform
from player import Player
from constants import *
import pygame

class health_bar(Entity):
    def __init__(self):
        self.health = Player.health

    def draw(self):
        pass