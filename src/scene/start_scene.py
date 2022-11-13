from typing import Sequence, Tuple

import pygame as pg
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

from src.entity.abstract_entity import Transform
from src.entity.button import Button
from src.scene.scene import Scene
from src.scene.scene_id import SceneId

class StartScene(Scene):
    def __init__(self) -> None:
        self.start_button = Button(pg.image.load('.\image\start_button.png'), 0,0,Transform(0,pg.Vector2(SCREEN_WIDTH/2,SCREEN_HEIGHT/2),pg.Vector2(1,0)),lambda : print('a'))

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click:Tuple[int,int,int]) -> None:
        self.key_pressed = key_pressed
        self.mouse_pos = mouse_pos
        self.mouse_click = mouse_click
        self.start_button.update(key_pressed,mouse_pos,mouse_click)
        
        return
    
    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((255,255,255))
        screen.blit(self.start_button.image,self.start_button.rect.topleft)

    def check_scene_switch(self) -> SceneId | None:
        return None

    def start_scene(self) -> None:
        return

    def stop_scene(self) -> None:
        return
