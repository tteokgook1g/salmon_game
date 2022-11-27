import pygame as pg
import schedule  # type: ignore
from pygame.mixer import Sound

from src.entity.enemy import Boss
from src.entity.player import Player
from src.helper.update_info import UpdateInfo
from src.scene.scene import Stage
from src.scene.scene_id import SceneId


class Stage1(Stage):
    """스테이지 1번"""

    def __init__(self, player: Player, boss: Boss) -> None:
        super().__init__(player, boss, bossspawntime=3600,
                         tile=pg.image.load("image/Tile 1.png"), sound=Sound(
                             "sound/bgm/Different Heaven - Nekozilla [NCS Release].mp3"),
                         )

        self.normalspawntime = 240
        self.normalcooltime = 0
        self.bossspawntime = 3600
        self.sound.set_volume(0.2)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if self.boss.health <= 0:
            self.switch = SceneId.stage2_scene
            schedule.cancel_job(all)  # type: ignore
        self.collide()
        self.time += 1

        # 기본 적만 생성
        self.normalcooltime += 1
        if self.normalcooltime >= self.normalspawntime/self.difficulty:
            self.spawn_normal()
            self.normalcooltime = 0
        if self.time == self.bossspawntime:
            self.boss.transform.pos = self.position_set()

    def start_scene(self) -> None:
        super().start_scene()
