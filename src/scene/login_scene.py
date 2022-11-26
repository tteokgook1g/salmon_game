import pygame as pg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.helper.user_data import UserDataFileStream
from src.entity.player import BombSkill, LightningSkill, Player
from src.helper.update_info import UpdateInfo
from src.entity.textbox import TextBox
from src.entity.abstract_entity import Transform
from src.entity.button import Button
from src.entity.textinput import InputBox
from src.scene.scene import Scene
from src.scene.scene_id import SceneId


class LoginScene(Scene):
    def __init__(self, player: Player):
        self.player = player

    def action(self, typ: str):
        if typ == 'confirm_button':
            stream = UserDataFileStream()
            data = stream.get_userdata(self.txt)
            if data is None:
                self.switch = SceneId.stage1_scene
                return

            # Nickname Stage XP Level Money skill1 skill2
            self.switch=SceneId(data.scene)
            self.player.xp = data.xp
            self.player.level = data.level
            self.player.money = data.money
            self.player.stat.skill_point=data.skill_point

            if data.bomb_skill:
                self.player.skills['bomb'] = BombSkill(2)
            if data.lightning_skill:
                self.player.skills['lightning'] = LightningSkill(5)

        elif typ == 'id_button':
            self.txt = self.inputbox.text
            self.inputbox = TextBox(pg.font.Font(None, 40).render(self.txt, True, (0, 0, 0), (0, 0, 0)), 0, 0, Transform(
                0, pg.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50), pg.Vector2(1, 0)), self.txt, 40, (0, 0, 0))

    def update(self, info: UpdateInfo) -> None:
        self.switch = None
        self.confirm_button.update(info)
        self.inputbox.update(info)

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((255, 255, 255))
        screen.blit(self.confirm_button.image,
                    self.confirm_button.rect.topleft)
        screen.blit(self.textbox.image,self.textbox.rect.topleft)
        self.inputbox.draw(screen)

    def check_scene_switch(self) -> SceneId | None:
        return self.switch

    def start_scene(self) -> None:
        self.txt = ''

        self.confirm_button = Button(pg.font.Font(None, 35).render('confirm', True, (255, 255, 255), (0, 0, 0)), 0, 0, Transform(
            0, pg.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50), pg.Vector2(1, 0)), lambda: self.action('confirm_button'))
        self.inputbox = InputBox(pg.font.Font(None, 40).render(self.txt, True, (0, 0, 0), (0, 0, 0)), 0, 0, Transform(
            0, pg.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50), pg.Vector2(1, 0)), self.txt, 40, (0, 0, 0), lambda: self.action('id_button'))
        self.textbox = TextBox(pg.font.Font(None, 40).render('input your nickname here',True,(0, 0, 0)), 1,0,Transform(0, pg.Vector2(
            SCREEN_WIDTH/2, SCREEN_HEIGHT/2-100), pg.Vector2(1, 0)), 'input your nickname here', 40, (0, 0, 0))

    def stop_scene(self) -> None:
        return
