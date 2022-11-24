import random

import pygame as pg
import schedule  # type: ignore
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame.rect import Rect
from pygame.surface import Surface

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_WIDTH, WORLD_BORDER
from src.entity.abstract_entity import Reward, Transform
from src.entity.enemy import Boss, BossSkillParticle, Enemy
from src.entity.player import GunSkill, Player, SkillParticle
from src.entity.shop.shop import Shop
from src.helper.camera_surface import CameraSurface
from src.helper.group import Group
from src.helper.update_info import UpdateInfo
from src.scene.scene import Scene
from src.scene.scene_id import SceneId


class Stage1(Scene):
    """abstract class representing game stages."""
    __slots__ = ("player", "enemies", "skill_particles",
                 "camera_surface", "rewards", "boss")
    player: Player
    enemies: Group[Enemy]
    skill_particles: Group[SkillParticle]
    boss_particles: Group[BossSkillParticle]
    rewards: Group[Reward]
    camera_surface: CameraSurface
    boss: Boss

    def __init__(self, player: Player, boss: Boss) -> None:
        super().__init__()
        self.player = player
        self.enemies = Group()
        self.skill_particles = Group()
        self.boss_particles = Group()
        self.rewards = Group()
        self.camera_surface = CameraSurface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), player.transform)
        self.switch = None
        self.time = 0
        self.difficulty = 0
        self.shop = Shop(player)
        self.player.money = 100
        self.boss = boss
        self.bossspawn = False
        self.time = 0
        self.bossspawntime = 3600
        self.tile = pg.image.load("image/Tile 1.png")
        self.sound = Sound(
            "sound/bgm/Different Heaven - Nekozilla [NCS Release].mp3")
        self.sound.set_volume(0.2)

    def update(self, info: UpdateInfo) -> None:
        schedule.run_pending()
        info.player = self.player
        self.player.update(info)
        self.camera_surface.update()
        self.boss.update(info)
        for enemy in self.enemies:
            enemy.update(info)
        for particle in self.skill_particles:
            particle.update(info)
        for reward in self.rewards:
            reward.update(info)
        for particle in self.boss_particles:
            particle.update(info)
        if self.player.health <= 0:
            self.player.health += 100
            self.switch = SceneId.end_scene
            schedule.cancel_job(all)  # type: ignore
        if self.boss.health <= 0:
            self.switch = SceneId.stage2_scene
            schedule.cancel_job(all)  # type: ignore
        self.collide()
        self.time += 1

        normal_particle_img = Surface((10, 10))
        normal_particle_img.fill((255, 0, 0))
        if self.time % 600 == 0:
            self.difficulty += 1
        if self.time % 120 == 0:
            self.spawn_normal()
        if self.time == self.bossspawntime:
            self.boss.transform.pos = Vector2([100, 100])

    def update_paused(self, info: UpdateInfo) -> None:
        self.shop.update(info)

    def draw(self, screen: pg.surface.Surface) -> None:
        self.camera_surface.fill((255, 255, 255))
        self.draw_on_camera_surface(self.camera_surface)
        screen.blit(self.camera_surface, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw_paused(self, screen: pg.surface.Surface) -> None:
        self.shop.draw(screen)

    def collide(self):
        for enemy in self.enemies:
            if pg.sprite.collide_rect(self.player, enemy):
                enemy.handle_collide(self.player)

        for boss_particle in self.boss_particles:
            if pg.sprite.collide_rect(self.player, boss_particle):
                boss_particle.handle_collide(self.player)

        if pg.sprite.collide_rect(self.player, self.boss) and self.time >= self.bossspawntime:
            self.boss.handle_collide(self.player)

        for reward in self.rewards:
            if pg.sprite.collide_rect(self.player, reward):
                reward.handle_collide(self.player)

        for particle in self.skill_particles:
            for enemy in self.enemies:
                if particle.check_collide(enemy):
                    particle.handle_collide(enemy)
            if particle.check_collide(self.boss) and self.time >= self.bossspawntime:
                particle.handle_collide(self.boss)

    def draw_on_camera_surface(self, camera_surface: CameraSurface) -> None:
        """implement it to draw entities"""
        self._draw_background(camera_surface)
        for enemy in self.enemies:
            enemy.draw(camera_surface)
        for particle in self.skill_particles:
            particle.draw(camera_surface)
        for particle in self.boss_particles:
            particle.draw(camera_surface)
        for reward in self.rewards:
            reward.draw(camera_surface)
        self.player.draw(camera_surface)
        if self.time - 1 >= self.bossspawntime:
            self.boss.draw(camera_surface)

    def _draw_background(self, camera_surface: CameraSurface):
        rect = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        rect.center = int(camera_surface.pos.x), int(
            camera_surface.pos.y)
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

        gun_skill = GunSkill(10)
        self.player.skills["gun"] = gun_skill
        gun_skill.bind(self.skill_particles, self.player)
        self.player.skill_particles = self.skill_particles
        Enemy.reward_group = self.rewards
        Boss.reward_group = self.rewards

        self.sound.play(-1)

    def position_set(self):
        pos = random.randint(50, WORLD_BORDER-50)
        direction = random.randint(1, 4)
        if direction == 1:
            return Vector2(50, pos)
        elif direction == 2:
            return Vector2(WORLD_BORDER-50, pos)
        elif direction == 3:
            return Vector2(pos, 50)
        else:
            return Vector2(pos, WORLD_BORDER-50)

    def spawn_normal(self) -> None:
        """spawn enemy"""
        normal_img = Surface((30, 30))
        normal_img.fill((0, 200, 0))
        pg.draw.rect(normal_img, (70, 20, 0), (0, 0, 30, 30), 3)
        self.enemies.add(Enemy(normal_img, 100 + self.difficulty, 10 + self.difficulty, Transform(
            1 + min(self.difficulty * 0.02, 0.3), self.position_set(), Vector2(0, 1))))

    def spawn_rare(self) -> None:
        rare_img = Surface((35, 35))
        rare_img.fill((0, 0, 200))
        pg.draw.rect(rare_img, (70, 20, 0), (0, 0, 35, 35), 3)
        self.enemies.add(Enemy(rare_img, 150 + self.difficulty, 15 + self.difficulty, Transform(
            1.4 + min(self.difficulty * 0.02, 0.3), self.position_set(), Vector2(0, 1))))

    def spawn_epic(self) -> None:
        epic_img = Surface((40, 40))
        epic_img.fill((200, 0, 200))
        pg.draw.rect(epic_img, (70, 20, 0), (0, 0, 40, 40), 3)
        self.enemies.add(Enemy(epic_img, 400 + self.difficulty, 20 + self.difficulty, Transform(
            1.8 + min(self.difficulty * 0.02, 0.3), self.position_set(), Vector2(0, 1))))

    def stop_scene(self) -> None:
        self.sound.stop()
