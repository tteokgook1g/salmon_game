import pygame as pg
from pygame import Vector2
from pygame.surface import Surface

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WORLD_BORDER
from src.entity.abstract_entity import Transform
from src.entity.enemy.basicEnemy import Enemy
from src.entity.player import Player, SkillParticle
from src.helper.camera_surface import CameraSurface
from src.helper.group import Group
from src.helper.update_info import UpdateInfo
from src.scene.scene import Scene
from src.scene.scene_id import SceneId


class Stage(Scene):
    """abstract class representing game stages."""
    __slots__ = ("player", "enemies", "skill_particles", "camera_surface")
    player: Player
    enemies: Group[Enemy]
    skill_particles: Group[SkillParticle]
    camera_surface: CameraSurface

    def __init__(self, player: Player) -> None:
        super().__init__()
        self.player = player
        self.enemies = Group()
        self.skill_particles = Group()
        self.camera_surface = CameraSurface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), player.transform)
        self.switch = None
        self.background = Surface((WORLD_BORDER, WORLD_BORDER))
        self.background.fill((240, 240, 240))

    def update(self, info: UpdateInfo) -> None:
        info.player = self.player
        self.player.update(info)
        for enemy in self.enemies:
            enemy.update(info)
        for particle in self.skill_particles:
            particle.update(info)
        if self.player.health < 0:
            self.switch = SceneId.end_scene
        self.collide()

    def draw(self, screen: pg.surface.Surface) -> None:
        self.camera_surface.fill((255, 255, 255))
        self.draw_on_camera_surface(self.camera_surface)
        screen.blit(self.camera_surface, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def collide(self):
        for enemy in self.enemies:
            if pg.sprite.collide_rect(self.player, enemy):
                self.player.handle_collide(enemy)
                enemy.transform.velocity *= -10
                enemy.transform.move()
                enemy.transform.velocity /= -10
        for particle in self.skill_particles:
            if pg.sprite.collide_rect(self.player, particle):
                pass

    def draw_on_camera_surface(self, camera_surface: CameraSurface) -> None:
        """implement it to draw entities"""
        border = Surface((WORLD_BORDER+2, WORLD_BORDER+2))
        border.fill((0, 0, 0))
        camera_surface.blit(border, pg.rect.Rect(-1, -1,
                            WORLD_BORDER+2, WORLD_BORDER+2))
        camera_surface.blit(self.background, pg.rect.Rect(
            0, 0, WORLD_BORDER, WORLD_BORDER))
        camera_surface.blit(self.player.image, self.player.rect)
        for enemy in self.enemies:
            camera_surface.blit(enemy.image, enemy.rect)
        for particle in self.skill_particles:
            camera_surface.blit(particle.image, particle.rect)

    def check_scene_switch(self) -> SceneId | None:
        return self.switch

    def start_scene(self) -> None:
        enemy_img = Surface((30, 30))
        enemy_img.fill((0, 200, 0))
        self.enemies.add(Enemy(enemy_img, 1, 1, Transform(
            1, Vector2(50, 50), Vector2(0, 1)), 10))
        return

    def stop_scene(self) -> None:
        return
