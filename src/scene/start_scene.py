from typing import Sequence, Tuple

import pygame as pg
from pygame.event import Event

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entity.abstract_entity import Transform
from src.entity.button import Button
from src.scene.scene import Scene
from src.scene.scene_id import SceneId


class StartScene(Scene):
    def action(self, typ: str):
        if typ == 'start_button':
            self.switch = SceneId.login_scene

    def __init__(self):
        self.start_scene()

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click: Tuple[int, int, int], events: Sequence[Event]) -> None:
        self.key_pressed = key_pressed
        self.mouse_pos = mouse_pos
        self.mouse_click = mouse_click
        self.switch = None
        self.start_button.update(key_pressed, mouse_pos, mouse_click, events)

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((255, 255, 255))
        screen.blit(self.start_button.image, self.start_button.rect.topleft)

    def check_scene_switch(self) -> SceneId | None:
        return self.switch

    def start_scene(self) -> None:
        self.start_button = Button(pg.image.load('./image/start_button.png'), 0, 0, Transform(0, pg.Vector2(
            SCREEN_WIDTH/2, SCREEN_HEIGHT/2), pg.Vector2(1, 0)), lambda: self.action('start_button'))

    def stop_scene(self) -> None:
        return
