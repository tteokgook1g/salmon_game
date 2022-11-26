import pygame as pg
import schedule  # type: ignore
from pygame.mixer import Sound

from src.entity.enemy import Boss
from src.entity.player import Player
from src.helper.update_info import UpdateInfo
from src.scene.scene import SceneManager, Stage
from src.scene.scene_id import SceneId


class Stage2(Stage):
    def __init__(self, player: Player, boss: Boss, scene_manager : SceneManager) -> None:
        super().__init__(player, boss, bossspawntime=3600,
                         tile=pg.image.load("image/Tile 2.png"),
                         sound=Sound(
                             "sound/bgm/Diviners - Savannah (feat. Philly K) [NCS Release].mp3"),
                             scene_manager = scene_manager)

        self.normalspawntime = 150
        self.normalcooltime = 0
        self.rarespawntime = 480
        self.rarecooltime = 0
        self.bossspawntime = 3900
        self.sound.set_volume(0.2)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if self.boss.health <= 0:
            self.switch = SceneId.stage3_scene
            schedule.cancel_job(all)  # type: ignore
        self.collide()
        self.time += 1

        self.normalcooltime += 1
        self.rarecooltime += 1
        if self.normalcooltime >= self.normalspawntime/self.difficulty:
            self.spawn_normal()
            self.normalcooltime = 0
        if self.rarecooltime >= self.rarespawntime/self.difficulty:
            self.spawn_rare()
            self.rarecooltime = 0
        if self.time == self.bossspawntime:
            self.boss.transform.pos = self.position_set()