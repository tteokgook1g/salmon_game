import pygame as pg
from typing import Tuple
from pygame import Rect, Surface
from pyparsing import Sequence
from helper.update_info import UpdateInfo
from src.entity.abstract_entity import Entity, Transform

class health_bar(Entity):
    def __init__(self, entity: Entity):
        self.entity = entity
        self.rect = pg.rect.Rect(0,0,40,10)
        
    def update(self, info: UpdateInfo) -> None:
        self.health = self.entity.health
        self.transform = self.entity.transform
        self.transform.pos.y -= 40
        self.rect.center = int(self.transform.pos.x), int(self.transform.pos.y)
        if self.health < 0:
            self.kill()
    
