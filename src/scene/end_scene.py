
import pygame as pg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.helper.update_info import UpdateInfo
from src.entity.abstract_entity import Transform
from src.entity.button import Button
from src.scene.scene import Scene
from src.scene.scene_id import SceneId
from src.scene.stage_scene import Stage

class EndScene(Scene):
    def action(self, typ: str):
        if typ == 'start_button':
            self.switch = SceneId.login_scene

    def __init__(self):
        self.start_scene()

    def update(self, info: UpdateInfo) -> None:
        self.key_pressed = info.key_pressed
        self.mouse_pos = info.mouse_pos
        self.mouse_click = info.mouse_click
        self.switch = None
        self.start_button.update(info)

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
