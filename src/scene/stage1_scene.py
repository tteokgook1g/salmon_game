import pygame as pg
import schedule  # type: ignore
from pygame.mixer import Sound

from src.entity.enemy import Boss
from src.entity.player import Player
from src.helper.update_info import UpdateInfo
from src.scene.scene import SceneManager, Stage
from src.scene.scene_id import SceneId


class Stage1(Stage):
    """abstract class representing game stages."""

    def __init__(self, player: Player, boss: Boss, scene_manager: SceneManager) -> None:
        super().__init__(player, boss, bossspawntime=3600,
                         tile=pg.image.load("image/Tile 1.png"), sound=Sound(
                             "sound/bgm/Different Heaven - Nekozilla [NCS Release].mp3"),
                         scene_manager=scene_manager)

        self.normalspawntime = 180
        self.normalcooltime = 0
        self.bossspawntime = 2700
        self.sound.set_volume(0.2)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if self.boss.health <= 0:
            self.switch = SceneId.stage2_scene
            schedule.cancel_job(all)  # type: ignore
        self.collide()
        self.time += 1

        self.normalcooltime += 1
        if self.normalcooltime >= self.normalspawntime/self.difficulty:
            self.spawn_normal()
            self.normalcooltime = 0
        if self.time == self.bossspawntime:
            self.boss.transform.pos = self.position_set()

    def start_scene(self) -> None:
        super().start_scene()
