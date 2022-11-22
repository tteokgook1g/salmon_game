
import subprocess, os, sys
import pygame as pg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entity.player import Player
from src.entity.textbox import TextBox
from src.helper.update_info import UpdateInfo
from src.entity.abstract_entity import Transform
from src.scene.scene import Scene, SceneManager
from src.scene.scene_id import SceneId


class EndScene(Scene):
    def __init__(self,player:Player, scene_manager:SceneManager) -> None:
        super().__init__()
        self.player = player
        self.scene_manager = scene_manager

    def action(self, typ: str):
        if typ == 'start_button':
            self.switch = SceneId.login_scene

    def update(self, info: UpdateInfo) -> None:
        self.switch = None
        if info.key_pressed[pg.K_r]:
            print(os.path.realpath(__file__))
            s=os.path.realpath(__file__).split(os.sep)[:-3]
            s.append('main.py')
            print(s)
            s=os.sep.join(s)
            print(s)
            subprocess.call([sys.executable, s] + sys.argv[1:])
            self.scene_manager.running=False


    def draw(self, screen: pg.surface.Surface) -> None:
        screen.blit(self.backgroundimg,(0,0))
        screen.blit(self.scorebox.image,self.scorebox.rect.topleft)

    def check_scene_switch(self) -> SceneId | None:
        return self.switch

    def start_scene(self) -> None:
        self.scorebox = TextBox(pg.font.Font(None, 40).render(f'Your Score : {self.player.xp}',True,(255,255,255)), 1,0,Transform(0, pg.Vector2(
            SCREEN_WIDTH/2, SCREEN_HEIGHT/2+200), pg.Vector2(1, 0)), f'Your Score : {self.player.xp}', 40, (255,255,255))
        self.backgroundimg = pg.image.load('./image/Game Over.jpg')

    def stop_scene(self) -> None:
        return