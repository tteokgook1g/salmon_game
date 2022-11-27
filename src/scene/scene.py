"""defines Abstract class Scene, class Stage, class SceneManager"""

import random
from abc import ABC, abstractmethod
from typing import Dict, Tuple

import pygame as pg
import schedule  # type: ignore
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame.rect import Rect
from pygame.surface import Surface

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_WIDTH, WORLD_BORDER
from src.entity.abstract_entity import Reward, Transform
from src.entity.enemy import Boss, Enemy
from src.entity.health_bar import BossHealthBar, PlayerHealthBar
from src.entity.player import Player, PlayerStat, SkillParticle
from src.entity.shop.shop import Shop
from src.entity.textbox import TextBox2
from src.helper.camera_surface import CameraSurface
from src.helper.functions import vector_to_tuple
from src.helper.group import Group
from src.helper.update_info import UpdateInfo
from src.helper.user_data import UserData, UserDataFileStream
from src.scene.scene_id import SceneId


class Scene(ABC):
    """interface Scene"""
    __slots__ = ("_scene_manager", "player")

    def __init__(self, player: Player):
        self.player = player

    @property
    def scene_manager(self) -> "SceneManager":
        return self._scene_manager

    @scene_manager.setter
    def scene_manager(self, value: "SceneManager"):
        self._scene_manager = value

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


class SceneManager:
    """manages scenes and game"""
    __slots__ = ("player", "scenes", "current_id", "screen",
                 "timer", "paused", 'running')

    def __init__(self, initial_scene_id: SceneId, screen: pg.surface.Surface, player: Player):
        self.player = player
        self.scenes: Dict[SceneId, Scene] = {}
        self.current_id: SceneId = initial_scene_id
        self.screen = screen
        self.timer = pg.time.Clock()
        self.paused: bool = False
        self.running = True

        def set_pause(*args, **kwargs):  # type: ignore
            self.paused = True
        PlayerStat.set_pause = set_pause

    def add_scene(self, scene_id: SceneId, scene: Scene) -> None:
        """add a scene to the scene manager"""
        self.scenes[scene_id] = scene
        scene.scene_manager = self

    def update(self, info: UpdateInfo) -> None:
        """update current scene. you can use key and mouse if you need. """
        scene = self.scenes[self.current_id]
        scene.update(info)

        next_id = scene.check_scene_switch()
        if next_id is not None:
            scene.stop_scene()
            self.current_id = next_id
            self.scenes[next_id].start_scene()

    def update_paused(self, info: UpdateInfo) -> None:
        """when paused, update current scene. you can use key and mouse if you need. """
        scene = self.scenes[self.current_id]
        scene.update_paused(info)

        next_id = scene.check_scene_switch()
        if next_id is not None:
            scene.stop_scene()
            self.current_id = next_id
            self.scenes[next_id].start_scene()

    def draw(self, screen: pg.surface.Surface) -> None:
        """draw current scene on screen."""
        self.scenes[self.current_id].draw(screen)

    def draw_paused(self):
        self.draw(self.screen)
        temp = Surface((1280, 720))
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

        # save data
        self.save_userdata()

    def save_userdata(self):
        stat = self.player.stat
        nickname: str = self.scenes[SceneId.login_scene].txt  # type: ignore
        data = UserData(
            nickname,
            stat.scene,
            stat.xp,
            stat.money,
            stat.level,
            stat.skill_point,
            "bomb" in self.player.skills,
            "lightning" in self.player.skills,
            self.player.fullhp,
            self.player.transform.velocity,
            self.player.shootspeed
        )
        stream = UserDataFileStream()
        stream.append_userdata(data)


class Stage(Scene):
    """base class for all stages"""
    __slots__ = ("player", "enemies", "skill_particles", "boss_particles", "rewards", "camera_surface",
                 "switch", "time", "difficulty", "shop", "boss", "bossspawn", "time", "cooltime", "bossspawntime", "tile", "sound", 'scene_manager')

    def __init__(self, player: Player, boss: Boss, bossspawntime: int, tile: Surface, sound: Sound):
        super().__init__(player)
        self.enemies: Group[Enemy] = Group()
        self.skill_particles: Group[SkillParticle] = Group()
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
        self.congratulations = False
        self.hpbar = PlayerHealthBar(player)
        self.bosshpbar = BossHealthBar(boss)

    def update(self, info: UpdateInfo) -> None:
        schedule.run_pending()
        info.player = self.player
        self.player.update(info)
        self.camera_surface.update()
        self.boss.update(info)
        self.hpbar.update()
        if self.bossspawn == True:
            self.bosshpbar.update()
        for enemy in self.enemies:
            enemy.update(info)
        for particle in self.skill_particles:
            particle.update(info)
        for reward in self.rewards:
            reward.update(info)
        if self.player.health <= 0:
            self.player.health += 100
            self.switch = SceneId.end_scene
            schedule.cancel_job(all)  # type: ignore
        if self.time % 1200 == 0:
            self.difficulty += 0.1
        if self.time >= self.bossspawntime:
            self.bossspawn = True

        self.hptext = TextBox2(pg.font.Font(None, 40).render(f'HP : {self.player.health}/{self.player.fullhp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 40), pg.Vector2(1, 0)), f'HP : {self.player.health}/{self.player.fullhp}', 20, (0, 0, 0))
        self.moneytext = TextBox2(pg.font.Font(None, 40).render(f'MONEY : {self.player.money}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 60), pg.Vector2(1, 0)), f'MONEY : {self.player.money}', 20, (0, 0, 0))
        self.xptext = TextBox2(pg.font.Font(None, 40).render(f'XP : {self.player.xp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 80), pg.Vector2(1, 0)), f'XP : {self.player.xp}', 20, (0, 0, 0))
        self.bosshptext = TextBox2(pg.font.Font(None, 40).render(f'BOSS HP : {self.boss.health}/{self.boss.fullhp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            SCREEN_WIDTH - 40, 40), pg.Vector2(1, 0)), f'BOSS HP : {self.boss.health}/{self.boss.fullhp}', 20, (0, 0, 0))

    def update_paused(self, info: UpdateInfo) -> None:
        self.shop.update(info)
        if self.bossspawn == True:
            self.bosshpbar.update()

        self.hptext = TextBox2(pg.font.Font(None, 40).render(f'HP : {self.player.health}/{self.player.fullhp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 40), pg.Vector2(1, 0)), f'HP : {self.player.health}/{self.player.fullhp}', 20, (0, 0, 0))
        self.moneytext = TextBox2(pg.font.Font(None, 40).render(f'MONEY : {self.player.money}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 60), pg.Vector2(1, 0)), f'MONEY : {self.player.money}', 20, (0, 0, 0))
        self.xptext = TextBox2(pg.font.Font(None, 40).render(f'XP : {self.player.xp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 80), pg.Vector2(1, 0)), f'XP : {self.player.xp}', 20, (0, 0, 0))
        self.bosshptext = TextBox2(pg.font.Font(None, 40).render(f'BOSS HP : {self.boss.health}/{self.boss.fullhp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            SCREEN_WIDTH - 40, 40), pg.Vector2(1, 0)), f'BOSS HP : {self.boss.health}/{self.boss.fullhp}', 20, (0, 0, 0))
        

    def draw(self, screen: pg.surface.Surface) -> None:
        self.camera_surface.fill((255, 255, 255))
        self.draw_on_camera_surface(self.camera_surface)
        screen.blit(self.camera_surface, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        self.hpbar.draw(screen)
        if self.bossspawn == True:
            self.bosshpbar.draw(screen)
            self.bosshptext.draw(screen)
        self.hptext.draw(screen)
        self.xptext.draw(screen)
        self.moneytext.draw(screen)

    def draw_paused(self, screen: pg.surface.Surface) -> None:
        self.shop.draw(screen)

        self.hpbar.draw(screen)
        if self.bossspawn == True:
            self.bosshpbar.draw(screen)
            self.bosshptext.draw(screen)
        self.hptext.draw(screen)
        self.xptext.draw(screen)
        self.moneytext.draw(screen)

    def collide(self):
        for enemy in self.enemies:
            if pg.sprite.collide_rect(self.player, enemy):
                enemy.handle_collide(self.player)

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
        for reward in self.rewards:
            reward.draw(camera_surface)
        self.player.draw(camera_surface)
        if self.time - 1 >= self.bossspawntime:
            self.boss.draw(camera_surface)

    def _draw_background(self, camera_surface: CameraSurface):
        rect = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        rect.center = vector_to_tuple(camera_surface.pos)
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
        """make to go to next stage"""
        return self.switch

    def start_scene(self) -> None:

        for skill in self.player.skills.values():
            skill.bind(self.skill_particles, self.player)
        self.sound.play(-1)

        Enemy.reward_group = self.rewards
        Boss.reward_group = self.rewards

        self.player.skill_particles = self.skill_particles

        self.hptext = TextBox2(pg.font.Font(None, 40).render(f'HP : {self.player.health}/{self.player.fullhp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 40), pg.Vector2(1, 0)), f'HP : {self.player.health}/{self.player.fullhp}', 20, (0, 0, 0))
        self.moneytext = TextBox2(pg.font.Font(None, 40).render(f'MONEY : {self.player.money}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 60), pg.Vector2(1, 0)), f'MONEY : {self.player.money}', 20, (0, 0, 0))
        self.xptext = TextBox2(pg.font.Font(None, 40).render(f'XP : {self.player.xp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            100, 80), pg.Vector2(1, 0)), f'XP : {self.player.xp}', 20, (0, 0, 0))
        self.bosshptext = TextBox2(pg.font.Font(None, 40).render(f'BOSS HP : {self.boss.health}/{self.boss.fullhp}', True, (0, 0, 0)), 1, 0, Transform(0, pg.Vector2(
            SCREEN_WIDTH - 40, 40), pg.Vector2(1, 0)), f'BOSS HP : {self.boss.health}/{self.boss.fullhp}', 20, (0, 0, 0))

    def position_set(self):
        """set enemy spawn position"""
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
        """spawn normal enemy"""
        normal_img = pg.image.load("image/NormalEnemy.png")
        self.enemies.add(Enemy(normal_img, 100, 10, Transform(
            1, self.position_set(), Vector2(0, 1)), 2))

    def spawn_rare(self) -> None:
        """spawn rare enemy"""
        rare_img = pg.image.load("image/RareEnemy.png")
        self.enemies.add(Enemy(rare_img, 150, 15, Transform(
            1.4, self.position_set(), Vector2(0, 1)), 5))

    def spawn_epic(self) -> None:
        """spawn epic enemy"""
        epic_img = pg.image.load("image/EpicEnemy.png")
        self.enemies.add(Enemy(epic_img, 400, 20, Transform(
            1.8, self.position_set(), Vector2(0, 1)), 12))

    def spawn_rush(self) -> None:
        """spawn rush enemy"""
        rush_img = pg.image.load("image/RushEnemy.png")
        self.enemies.add(Enemy(rush_img, 10, 1, Transform(
            5, self.position_set(), Vector2(0, 1)), 3))

    def spawn_tank(self) -> None:
        """spawn rush enemy"""
        tank_img = pg.image.load("image/TankEnemy.png")
        self.enemies.add(Enemy(tank_img, 1000, 1, Transform(
            0.5, self.position_set(), Vector2(0, 1)), 9))

    def stop_scene(self) -> None:
        """sound stop when scene changes"""
        self.sound.stop()
        self.player.stat.scene = self.scene_manager.current_id
