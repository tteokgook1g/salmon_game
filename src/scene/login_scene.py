from typing import Sequence, Tuple

import pygame as pg
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

from src.entity.abstract_entity import Transform
from src.entity.button import Button
from src.scene.scene import Scene
from src.scene.scene_id import SceneId

class LoginScene(Scene):
        
    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click:Tuple[int,int,int]) -> None:
        self.key_pressed = key_pressed
        self.mouse_pos = mouse_pos
        self.mouse_click = mouse_click
        self.confirm_button.update(key_pressed,mouse_pos,mouse_click)
        
        return
    
    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((255,255,255))
        screen.blit(self.confirm_button.image,self.confirm_button.rect.topleft)

    def check_scene_switch(self) -> SceneId | None:
        return None

    def start_scene(self) -> None:
        self.confirm_button = Button(pg.font.Font(None,35).render('confirm',True,(0,0,0),(255,0,0)), 0,0,Transform(0,pg.Vector2(SCREEN_WIDTH/2,SCREEN_HEIGHT/2),pg.Vector2(1,0)),lambda : print('a'))

    def stop_scene(self) -> None:
        return
