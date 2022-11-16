"""defines Abstract class Scene, class Stage, class SceneManager"""

from abc import ABC, abstractmethod
from typing import Dict, Sequence, Tuple

import pygame as pg
from pygame.event import Event
from src.scene.scene_id import SceneId


class Scene(ABC):
    """interface Scene"""
    @abstractmethod
    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click: Tuple[int, int, int], events: Sequence[Event]) -> None:
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

    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int], mouse_click: Tuple[int, int, int], events: Sequence[Event]) -> None:
        """update current scene. you can use key and mouse if you need. """
        scene = self.scenes[self.current_id]
        scene.update(key_pressed, mouse_pos, mouse_click, events)

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
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False

            key_pressed = pg.key.get_pressed()
            mouse_pos = pg.mouse.get_pos()
            mouse_click: Tuple[int, int,
                               int] = pg.mouse.get_pressed()  # type: ignore

            self.update(key_pressed, mouse_pos, mouse_click, events)
            
            self.draw(self.screen)

            pg.display.update()
            self.timer.tick(60)

        self.scenes[self.current_id].stop_scene()