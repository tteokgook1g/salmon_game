import pygame as pg
import schedule  # type: ignore
from pygame.math import Vector2
from pygame.mixer import Sound

from src.entity.enemy import Boss
from src.entity.player import Player
from src.helper.update_info import UpdateInfo
from src.scene.scene import Stage
from src.scene.scene_id import SceneId


class Stage3(Stage):
    """abstract class representing game stages."""

    def __init__(self, player: Player, boss: Boss) -> None:
        super().__init__(player, boss, bossspawntime=3600,
                         tile=pg.image.load("image/Tile 3.png"),
                         sound=Sound(
                             "sound/bgm/DEAF KEV - Invincible [NCS Release].mp3")
                         )

        self.sound.set_volume(0.2)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if self.boss.health <= 0:
            self.switch = SceneId.stage3_scene
            schedule.cancel_job(all)  # type: ignore
        self.collide()
        self.time += 1

        if self.time % 600 == 0:
            self.difficulty += 1
        if self.time % 60 == 0:
            self.spawn_normal()
        if self.time % 240 == 0:
            self.spawn_rare()
        if self.time % 600 == 0:
            self.spawn_epic()
        if self.time == self.bossspawntime:
            self.boss.transform.pos = Vector2([100, 100])
