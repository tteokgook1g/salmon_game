"""defines Abstract class Scene, class Stage, class SceneManager"""

from abc import ABC, abstractmethod
import random
from typing import Dict, Tuple

import pygame as pg
import schedule  # type: ignore
from pygame.mixer import Sound
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.math import Vector2

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_WIDTH, WORLD_BORDER
from src.entity.abstract_entity import Reward, Transform
from src.entity.enemy import Boss, BossSkillParticle, Enemy
from src.entity.player import Player, SkillParticle
from src.entity.shop.shop import Shop
from src.helper.camera_surface import CameraSurface
from src.helper.group import Group
from src.helper.update_info import UpdateInfo
from src.scene.scene_id import SceneId


class Scene(ABC):
    """interface Scene"""
    @abstractmethod
    def update(self, info: UpdateInfo) -> None:
        """update the scene. you can use key and mouse if you need. """

    def update_paused(self, info: UpdateInfo) -> None:
        """when paused, update the scene. you can use key and mouse if you need. """
        pass

    @abstractmethod
    def draw(self, screen: pg.surface.Surface) -> None:
        """draw the scene on screen."""

    def draw_paused(self, screen: pg.surface.Surface) -> None:
        """when paused, draw the scene on screen after draw method called."""
        pass

    @abstractmethod
    def check_scene_switch(self) -> SceneId | None:
        """
        check if the scene need to switch to a different scene.
        it returns SceneId to switch to. it returns None if the scene do not need to switch to a different scene.
        """

    @abstractmethod
    def start_scene(self) -> None:
        """called when the scene is started"""

    @abstractmethod
    def stop_scene(self) -> None:
        """called when the scene is stopped"""


class Stage(Scene):
    """base class for all stages"""
    __slots__ = ("player", "enemies", "skill_particles", "boss_particles", "rewards", "camera_surface",
                 "switch", "time", "difficulty", "shop", "boss", "bossspawn", "time", "cooltime", "bossspawntime", "tile", "sound")

    def __init__(self, player: Player, boss: Boss, bossspawntime: int, tile: Surface, sound: Sound):
        super().__init__()
        self.player = player
        self.enemies: Group[Enemy] = Group()
        self.skill_particles: Group[SkillParticle] = Group()
        self.boss_particles: Group[BossSkillParticle] = Group()
        self.rewards: Group[Reward] = Group()
        self.camera_surface = CameraSurface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), player.transform)
        self.switch = None
        self.time = 0
        self.difficulty = 1
        self.shop = Shop(player)
        self.player.money = 0
        self.boss = boss
        self.bossspawn = False
        self.time = 0
        self.cooltime = 0
        self.bossspawntime = bossspawntime
        self.tile = tile
        self.sound = sound

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
        for skill in self.player.skills.values():
            skill.bind(self.skill_particles, self.player)
        self.sound.play(-1)

        Enemy.reward_group = self.rewards
        Boss.reward_group = self.rewards

        self.player.skill_particles = self.skill_particles

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
        self.enemies.add(Enemy(normal_img, 100, 10, Transform(
            1, self.position_set(), Vector2(0, 1)), 1))

    def spawn_rare(self) -> None:
        rare_img = Surface((35, 35))
        rare_img.fill((0, 0, 200))
        pg.draw.rect(rare_img, (70, 20, 0), (0, 0, 35, 35), 3)
        self.enemies.add(Enemy(rare_img, 15, 15, Transform(
            1.4, self.position_set(), Vector2(0, 1)), 2))

    def spawn_epic(self) -> None:
        epic_img = Surface((40, 40))
        epic_img.fill((200, 0, 200))
        pg.draw.rect(epic_img, (70, 20, 0), (0, 0, 40, 40), 3)
        self.enemies.add(Enemy(epic_img, 400, 20, Transform(
            1.8, self.position_set(), Vector2(0, 1)), 4))

    def stop_scene(self) -> None:
        self.sound.stop()


class SceneManager:
    """manages scenes and game"""
    __slots__ = ("scenes", "current_id", "screen",
                 "timer", "paused", 'running')

    def __init__(self, initial_scene_id: SceneId, screen: pg.surface.Surface):
        self.scenes: Dict[SceneId, Scene] = {}
        self.current_id: SceneId = initial_scene_id
        self.screen = screen
        self.timer = pg.time.Clock()
        self.paused: bool = False
        self.running = True

    def add_scene(self, scene_id: SceneId, scene: Scene) -> None:
        """add a scene to the scene manager"""
        self.scenes[scene_id] = scene

    def update(self, info: UpdateInfo) -> None:
        """update current scene. you can use key and mouse if you need. """
        scene = self.scenes[self.current_id]
        scene.update(info)

        next_id = scene.check_scene_switch()
        if next_id is not None:
            self.current_id = next_id
            scene.stop_scene()
            self.scenes[next_id].start_scene()

    def update_paused(self, info: UpdateInfo) -> None:
        """when paused, update current scene. you can use key and mouse if you need. """
        scene = self.scenes[self.current_id]
        scene.update_paused(info)

        next_id = scene.check_scene_switch()
        if next_id is not None:
            self.current_id = next_id
            scene.stop_scene()
            self.scenes[next_id].start_scene()

    def draw(self, screen: pg.surface.Surface) -> None:
        """draw current scene on screen."""
        self.scenes[self.current_id].draw(screen)

    def draw_paused(self):
        self.draw(self.screen)
        temp = Surface((800, 600))
        temp.set_alpha(128)
        temp.fill((100, 100, 100))
        self.screen.blit(temp, temp.get_rect())
        self.scenes[self.current_id].draw_paused(self.screen)

    def run(self):
        """runs the game loop"""
        self.scenes[self.current_id].start_scene()

        while self.running:
            events = pg.event.get()
            key_pressed = pg.key.get_pressed()
            mouse_pos = pg.mouse.get_pos()
            mouse_click: Tuple[int, int,
                               int] = pg.mouse.get_pressed()  # type: ignore

            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN and key_pressed[pg.K_ESCAPE]:
                    self.paused = not self.paused

            info = UpdateInfo(key_pressed, mouse_pos,
                              mouse_click, events, None, self.paused)

            if self.paused:
                self.draw_paused()
                self.update_paused(info)
            else:
                self.update(info)
                self.draw(self.screen)

            pg.display.update()
            self.timer.tick(60)

        self.scenes[self.current_id].stop_scene()
