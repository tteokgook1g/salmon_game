"""defines Abstract class Scene, class Stage, class SceneManager"""

from abc import ABC, abstractmethod
from typing import Dict, Sequence, Tuple
import pygame as pg
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.helper.camera_surface import CameraSurface
from src.entity.abstract_entity import Enemy
from src.entity.player import Player, SkillParticle
from src.helper.group import Group

from src.scene.scene_id import SceneId


class Scene(ABC):
    """interface Scene"""
    @abstractmethod
    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int]) -> None:
        """update the scene. you can use key and mouse if you need. """

    @abstractmethod
    def draw(self, screen: pg.surface.Surface) -> None:
        """draw the scene on screen."""

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
    __slots__ = ("scenes", "current_id", "screen", "timer")

    def __init__(self, initial_scene_id: SceneId, screen: pg.surface.Surface):
        self.scenes: Dict[SceneId, Scene] = {}
        self.current_id: SceneId = initial_scene_id
        self.screen = screen
        self.timer = pg.time.Clock()

    def add_scene(self, scene_id: SceneId, scene: Scene) -> None:
        """add a scene to the scene manager"""
        self.scenes[scene_id] = scene

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int]) -> None:
        """update current scene. you can use key and mouse if you need. """
        scene = self.scenes[self.current_id]
        scene.update(key_pressed, mouse_pos)

        next_id = scene.check_scene_switch()
        if next_id is not None:
            self.current_id = next_id
            scene.stop_scene()
            self.scenes[next_id].start_scene()

    def draw(self, screen: pg.surface.Surface) -> None:
        """draw current scene on screen."""
        self.scenes[self.current_id].draw(screen)

    def run(self):
        """runs the game loop"""
        self.scenes[self.current_id].start_scene()

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            key_pressed = pg.key.get_pressed()
            mouse_pos = pg.mouse.get_pos()
            self.update(key_pressed, mouse_pos)

            self.draw(self.screen)

            pg.display.update()
            self.timer.tick(60)

        self.scenes[self.current_id].stop_scene()


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

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int]) -> None:
        self.player.update(key_pressed, mouse_pos)
        for enemy in self.enemies:
            enemy.update(key_pressed, mouse_pos)
        for particle in self.skill_particles:
            particle.update(key_pressed, mouse_pos)

    def draw(self, screen: pg.surface.Surface) -> None:
        self.camera_surface.fill((255, 255, 255))
        self.draw_on_camera_surface(self.camera_surface)
        screen.blit(self.camera_surface, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw_on_camera_surface(self, camera_surface: CameraSurface) -> None:
        """implement it to draw entities"""
        camera_surface.blit(self.player.image, self.player.rect)
        for enemy in self.enemies:
            camera_surface.blit(enemy.image, enemy.rect)
        for particle in self.skill_particles:
            camera_surface.blit(particle.image, particle.rect)
