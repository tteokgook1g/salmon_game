import pygame as pg
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.mixer import Sound
import random as rd

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_WIDTH, WORLD_BORDER
from src.entity.abstract_entity import Reward, Transform
from src.entity.enemy.basicEnemy import Enemy
from src.entity.player import Player, SkillParticle
from src.helper.camera_surface import CameraSurface
from src.helper.group import Group
from src.helper.update_info import UpdateInfo
from src.scene.scene import Scene
from src.scene.scene_id import SceneId
import schedule


class Stage(Scene):
    """abstract class representing game stages."""
    __slots__ = ("player", "enemies", "skill_particles",
                 "camera_surface", "rewards")
    player: Player
    enemies: Group[Enemy]
    skill_particles: Group[SkillParticle]
    rewards: Group[Reward]
    camera_surface: CameraSurface

    def __init__(self, player: Player) -> None:
        super().__init__()
        self.player = player
        self.enemies = Group()
        self.skill_particles = Group()
        self.rewards = Group()
        self.camera_surface = CameraSurface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), player.transform)
        self.switch = None
        self.background = Surface((WORLD_BORDER, WORLD_BORDER))
        self.background.fill((240, 240, 240))
        self.time = 0
        self.difficulty = 0
        self.money = 0

        self.tile = pg.image.load("image/Tile 1.png")
        self.sound = Sound(
            "sound/bgm/Different Heaven - Nekozilla [NCS Release].mp3")
        self.sound.set_volume(0.1)

        # binding references
        Enemy.reward_group = self.rewards

    def update(self, info: UpdateInfo) -> None:
        schedule.run_pending()
        info.player = self.player
        self.player.update(info)
        for enemy in self.enemies:
            enemy.update(info)
        for particle in self.skill_particles:
            particle.update(info)
        if self.player.health <= 0:
            self.switch = SceneId.end_scene
            schedule.cancel_job(all)
        self.collide()
        self.time += 1
        if self.time % 1500 == 0:
            self.difficulty += 1
        if self.time % 300 == 0:
            self.normal_spawn()
        if self.time % 600 == 0:
            self.rare_spawn()
        if self.time % 1500 == 0:
            self.epic_spawn()
        if self.time == 6000:
            self.boss_spawn()

    def draw(self, screen: pg.surface.Surface) -> None:
        self.camera_surface.fill((255, 255, 255))
        self.draw_on_camera_surface(self.camera_surface)
        screen.blit(self.camera_surface, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def collide(self):
        for enemy in self.enemies:
            if pg.sprite.collide_rect(self.player, enemy):
                enemy.handle_collide(self.player)

        for reward in self.rewards:
            if pg.sprite.collide_rect(self.player, reward):
                reward.handle_collide(self.player)
                self.money += 100
                print(self.money)

        for particle in self.skill_particles:
            for enemy in self.enemies:
                if pg.sprite.collide_rect(particle, enemy):
                    particle.handle_collide(enemy)

    def draw_on_camera_surface(self, camera_surface: CameraSurface) -> None:
        """implement it to draw entities"""
        self._draw_background(camera_surface)
        for enemy in self.enemies:
            enemy.draw(camera_surface)
        for particle in self.skill_particles:
            particle.draw(camera_surface)
        for reward in self.rewards:
            reward.draw(camera_surface)
        self.player.draw(camera_surface)

    def _draw_background(self, camera_surface: CameraSurface):
        rect = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        rect.center = int(camera_surface.camera.pos.x), int(
            camera_surface.camera.pos.y)
        topleft = max(rect.left, 0), max(rect.top, 0)
        rightbottom = (min(rect.right, WORLD_BORDER),
                       min(rect.bottom, WORLD_BORDER))

        tl_tile = topleft[0]//TILE_WIDTH, topleft[1]//TILE_WIDTH-1
        rb_tile = ((rightbottom[0]-1)//TILE_WIDTH,
                   (rightbottom[1]-1)//TILE_WIDTH-1)
        tile_row_num: int = rb_tile[1]-tl_tile[1]+1
        tile_col_num: int = rb_tile[0]-tl_tile[0]+1

        row_tile: Surface = Surface((tile_col_num*TILE_WIDTH, TILE_WIDTH))
        row_rect = row_tile.get_rect()
        row_rect.topleft = tl_tile[0]*TILE_WIDTH, tl_tile[1]*TILE_WIDTH
        for i in range(tile_col_num):
            row_tile.blit(self.tile, (i*TILE_WIDTH, 0))
        for _ in range(tile_row_num):
            row_rect.top = row_rect.top+TILE_WIDTH
            camera_surface.blit(row_tile, row_rect)

    def check_scene_switch(self) -> SceneId | None:
        return self.switch

    def start_scene(self) -> None:
        normal_particle_img = Surface((10, 10))
        normal_particle_img.fill((255, 0, 0))
        self.normalparticle = schedule.every(1).seconds.do(lambda: self.skill_particles.add(SkillParticle(
            normal_particle_img, 1, 10, Transform(5, Vector2(self.player.transform.pos.xy), Vector2(1, 0)), self.player)))

        self.sound.play(-1)

        # spawn enemy
    def normal_spawn(self) -> None:
        normal_img = Surface((30, 30))
        normal_img.fill((0, 200, 0))
        pg.draw.rect(normal_img, (70, 20, 0), (0, 0, 30, 30), 3)
        self.enemies.add(Enemy(normal_img, 100 + self.difficulty, 10 + self.difficulty, Transform(
            1 + self.difficulty * 0.02, Vector2(50, 50), Vector2(0, 1))))

    def rare_spawn(self) -> None:
        rare_img = Surface((35, 35))
        rare_img.fill((0, 0, 200))
        pg.draw.rect(rare_img, (70, 20, 0), (0, 0, 35, 35), 3)
        self.enemies.add(Enemy(rare_img, 150 + self.difficulty, 12 + self.difficulty, Transform(
            1.1 + self.difficulty * 0.02, Vector2(50, 50), Vector2(0, 1))))

    def epic_spawn(self) -> None:
        epic_img = Surface((40, 40))
        epic_img.fill((200, 0, 200))
        pg.draw.rect(epic_img, (70, 20, 0), (0, 0, 40, 40), 3)
        self.enemies.add(Enemy(epic_img, 400, 15 + self.difficulty, Transform(
            1.2 + self.difficulty * 0.02, Vector2(50, 50), Vector2(0, 1))))

    def boss_spawn(self) -> None:
        boss_img = Surface((50, 50))
        boss_img.fill((200, 0, 0))
        pg.draw.rect(boss_img, (70, 20, 0), (0, 0, 50, 50), 3)
        self.enemies.add(Enemy(boss_img, 1000, 25, Transform(
            1.5, Vector2(50, 50), Vector2(0, 1))))

    def stop_scene(self) -> None:
        self.sound.stop()