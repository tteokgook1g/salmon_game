import pygame as pg
from pygame import Surface, Vector2
import copy
from src.entity.abstract_entity import Entity, Transform
from player import Player
from constants import *
import pygame

class health_bar():
    def __init__(self, entity: Entity):
        self.entity = entity
        self.fullhp = self.entity.fullhp
        self.health = self.entity.health
        self.transform = Transform(0,self.entity.transform.pos-Vector2(0,40),Vector2(1,0))

        
    def update(self) -> None:
        self.health = self.entity.health
        self.transform = Transform(0,self.entity.transform.pos-Vector2(0,40),Vector2(1,0))


    def draw(self):
        bar_rect=(60,10)
        hp_per = self.health/self.fullhp
        self.healthbar = []
        base = Surface((bar_rect[0]+2,bar_rect[1]+2))
        base.fill((0,0,0))
        hp = Surface((hp_per*bar_rect[0],bar_rect[1]))
        if hp_per<0.2:
            hp.fill((255,0,0))
        else:
            hp.fill((0,255,0))
        self.healthbar.append((base,pg.rect.Rect(self.transform.pos-Vector2(bar_rect[0]/2+1,bar_rect[1]/2+1),(bar_rect[0]+2,bar_rect[1]+2))))
        self.healthbar.append((hp,pg.rect.Rect(self.transform.pos.x-bar_rect[0]/2,self.transform.pos.y-bar_rect[1]/2,hp_per*bar_rect[0],bar_rect[1])))
        return self.healthbar

         