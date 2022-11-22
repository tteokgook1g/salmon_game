"""defines Abstract class Scene, class Stage, class SceneManager"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple

import pygame as pg
from src.helper.update_info import UpdateInfo
from src.scene.scene_id import SceneId
from pygame.surface import Surface


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


class SceneManager:
    """manages scenes and game"""
    __slots__ = ("scenes", "current_id", "screen", "timer", "paused",'running')

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
