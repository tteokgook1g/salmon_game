"""defines Abstract class Scene, class Stage, class SceneManager"""

from abc import ABC, abstractmethod
from typing import Dict, Sequence, Tuple
import pygame as pg
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
    """manages scenes"""
    __slots__ = ("scenes", "current_id")

    def __init__(self, initial_scene_id: SceneId):
        self.scenes: Dict[SceneId, Scene] = {}
        self.current_id: SceneId = initial_scene_id

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


class Stage(Scene):
    """abstract class representing game stages."""
    __slots__ = ("player", "enemies", "skill_particles")
    player: Player
    enemies: Group[Enemy]
    skill_particles: Group[SkillParticle]
