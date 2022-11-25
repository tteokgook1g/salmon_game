import pygame as pg
import schedule  # type: ignore
from pygame.math import Vector2
from pygame.mixer import Sound

from src.entity.enemy import Boss
from src.entity.player import GunSkill, Player
from src.helper.update_info import UpdateInfo
from src.scene.scene import Stage
from src.scene.scene_id import SceneId


class Stage1(Stage):
    """abstract class representing game stages."""

    def __init__(self, player: Player, boss: Boss) -> None:
        super().__init__(player, boss, bossspawntime=3600,
                         tile=pg.image.load("image/Tile 1.png"), sound=Sound(
                             "sound/bgm/Different Heaven - Nekozilla [NCS Release].mp3")
                         )

        self.sound.set_volume(0.2)

    def update(self, info: UpdateInfo) -> None:
        super().update(info)
        if self.boss.health <= 0:
            self.switch = SceneId.stage2_scene
            schedule.cancel_job(all)  # type: ignore
        self.collide()
        self.time += 1

        if self.time % 600 == 0:
            self.difficulty += 1
        if self.time % 120 == 0:
            self.spawn_normal()
        if self.time == self.bossspawntime:
            self.boss.transform.pos = Vector2([100, 100])

    def start_scene(self) -> None:
        super().start_scene()
        gun_skill = GunSkill(10)
        self.player.skills["gun"] = gun_skill
        gun_skill.bind(self.skill_particles, self.player)
        self.player.skill_particles = self.skill_particles
