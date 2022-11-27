
import pygame as pg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WORLD_BORDER
from src.entity.player import Player
from src.helper.update_info import UpdateInfo
from src.entity.abstract_entity import Transform
from src.entity.button import Button
from src.scene.scene import Scene
from src.scene.scene_id import SceneId
from src.entity.textbox import TextBox


class StartScene(Scene):
    def __init__(self, player: Player):
        super().__init__(player)
        self.start_scene()
        self.map = pg.rect.Rect(0, 0, WORLD_BORDER, WORLD_BORDER)

    def action(self, typ: str):
        if typ == 'start_button':
            self.switch = SceneId.login_scene

    def update(self, info: UpdateInfo) -> None:
        self.key_pressed = info.key_pressed
        self.mouse_pos = info.mouse_pos
        self.mouse_click = info.mouse_click
        self.switch = None
        self.start_button.update(info)

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.blit(pg.image.load('./image/salmon_is_delicious.jpg'), (0, 0))
        screen.blit(self.start_button.image, self.start_button.rect.topleft)
        screen.blit(self.textbox.image, self.textbox.rect.topleft)

    def check_scene_switch(self) -> SceneId | None:
        return self.switch

    def start_scene(self) -> None:
        self.start_button = Button(pg.image.load('./image/start_button.png'), 0, 0, Transform(0, pg.Vector2(
            SCREEN_WIDTH/2, SCREEN_HEIGHT/2), pg.Vector2(1, 0)), lambda: self.action('start_button'))
        self.textbox = TextBox(pg.font.Font(None, 100).render('End is salmon sashimi', True, (255, 255, 255)), 1, 0, Transform(0, pg.Vector2(
            SCREEN_WIDTH/2, SCREEN_HEIGHT/2-250), pg.Vector2(1, 0)), 'End is salmon sashimi', 100, (255, 255, 255))

    def stop_scene(self) -> None:
        return
