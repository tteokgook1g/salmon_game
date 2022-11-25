import pygame as pg
import schedule  # type: ignore
from pygame.math import Vector2
from pygame.mixer import Sound

from src.entity.enemy import Boss
from src.entity.player import Player
from src.helper.update_info import UpdateInfo
from src.scene.scene import Stage
from src.scene.scene_id import SceneId


class Stage2(Stage):
    """abstract class representing game stages."""

    def __init__(self, player: Player, boss: Boss) -> None:
        super().__init__(player, boss, bossspawntime=3600,
                         tile=pg.image.load("image/Tile 2.png"),
                         sound=Sound(
                             "sound/bgm/Diviners - Savannah (feat. Philly K) [NCS Release].mp3")
                         )

        self.normalspawntime = 180
        self.normalcooltime = 0
        self.rarespawntime = 360
        self.rarecooltime = 0
        self.bossspawntime = 5400
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
            self.boss.transform.pos = Vector2([100, 100])