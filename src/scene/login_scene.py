import pygame as pg

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.helper.update_info import UpdateInfo
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
                0, pg.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50), pg.Vector2(1, 0)), self.txt, 40, (0, 0, 0))

    def update(self, info: UpdateInfo) -> None:
        self.switch = None
<<<<<<< HEAD
        self.key_pressed = key_pressed
        self.mouse_pos = mouse_pos
        self.mouse_click = mouse_click
        self.confirm_button.update(key_pressed, mouse_pos, mouse_click, events)
        self.inputbox.update(key_pressed, mouse_pos, mouse_click, events)
        
=======
        self.key_pressed = info.key_pressed
        self.mouse_pos = info.mouse_pos
        self.mouse_click = info.mouse_click
        self.confirm_button.update(info)
        self.inputbox.update(info)
>>>>>>> 267167ae900ff126c928bf7d304a3782ff98c0f8

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
            0, pg.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50), pg.Vector2(1, 0)), self.txt, 40, (0, 0, 0), lambda: self.action('id_button'))

    def stop_scene(self) -> None:
        return
