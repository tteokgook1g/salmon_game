
import pygame as pg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entity.player import Player
from src.entity.textbox import TextBox
from src.helper.update_info import UpdateInfo
from src.entity.abstract_entity import Transform
from src.entity.button import Button
from src.scene.scene import Scene
from src.scene.scene_id import SceneId


class EndScene(Scene):
    def __init__(self,player:Player) -> None:
        super().__init__()
        self.player = player

    def action(self, typ: str):
        if typ == 'start_button':
            self.switch = SceneId.login_scene

    def update(self, info: UpdateInfo) -> None:
        self.key_pressed = info.key_pressed
        self.mouse_pos = info.mouse_pos
        self.mouse_click = info.mouse_click
        self.switch = None
        # self.start_button.update(info)

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.blit(self.backgroundimg,(0,0))
        # screen.blit(self.start_button.image, self.start_button.rect.topleft)
        screen.blit(self.scorebox.image,self.scorebox.rect.topleft)

    def check_scene_switch(self) -> SceneId | None:
        return self.switch

    def start_scene(self) -> None:
        '''
        self.start_button = Button(pg.image.load('./image/start_button.png'), 0, 0, Transform(0, pg.Vector2(
            SCREEN_WIDTH/2, SCREEN_HEIGHT/2+200), pg.Vector2(1, 0)), lambda: self.action('start_button'))
        '''
        self.scorebox = TextBox(pg.font.Font(None, 40).render(f'Your Score : {self.player.xp}',True,(255,255,255)), 1,0,Transform(0, pg.Vector2(
            SCREEN_WIDTH/2, SCREEN_HEIGHT/2+200), pg.Vector2(1, 0)), f'Your Score : {self.player.xp}', 40, (255,255,255))
        self.backgroundimg = pg.image.load('./image/Game Over.jpg')

    def stop_scene(self) -> None:
        return