from typing import Sequence, Tuple

import pygame as pg
from pygame.event import Event

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entity.textbox import TextBox
from src.entity.abstract_entity import Transform
from src.entity.button import Button
from src.entity.textinput import InputBox
from src.scene.scene import Scene
from src.scene.scene_id import SceneId


class LoginScene(Scene):

    def action(self, typ: str):
        if typ == 'confirm_button':
            self.switch = SceneId.stage_scene
        elif typ == 'id_button':
            self.txt = self.inputbox.text
            self.inputbox = TextBox(pg.font.Font(None, 40).render(self.txt, True, (0, 0, 0), (0, 0, 0)), 0, 0, Transform(
            0, pg.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50), pg.Vector2(1, 0)), self.txt,40,(0,0,0))

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click: Tuple[int, int, int], events: Sequence[Event]) -> None:
        self.switch = None
        self.key_pressed = key_pressed
        self.mouse_pos = mouse_pos
        self.mouse_click = mouse_click
        self.confirm_button.update(key_pressed, mouse_pos, mouse_click, events)
        self.inputbox.update(key_pressed, mouse_pos, mouse_click, events)
        

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((255, 255, 255))
        screen.blit(self.confirm_button.image,
                    self.confirm_button.rect.topleft)
        self.inputbox.draw(screen)

    def check_scene_switch(self) -> SceneId | None:
        return self.switch

    def start_scene(self) -> None:
        self.txt = 'input your nickname'
   
        self.confirm_button = Button(pg.font.Font(None, 35).render('confirm', True, (255, 255, 255), (0, 0, 0)), 0, 0, Transform(
            0, pg.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50), pg.Vector2(1, 0)), lambda: self.action('confirm_button'))
        self.inputbox = InputBox(pg.font.Font(None, 40).render(self.txt, True, (0, 0, 0), (0, 0, 0)), 0, 0, Transform(
            0, pg.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50), pg.Vector2(1, 0)), self.txt,40,(0,0,0),lambda: self.action('id_button'))
    def stop_scene(self) -> None:
        return
