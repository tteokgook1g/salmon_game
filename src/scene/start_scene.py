from typing import Sequence, Tuple
import pygame as pg

from src.scene.scene import Scene
from src.scene.scene_id import SceneId


class StartScene(Scene):
    def update(self, key_pressed: Sequence[bool], mouse_pos: Tuple[int, int]) -> None:
        return

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((255, 255, 255))

    def check_scene_switch(self) -> SceneId | None:
        return None

    def start_scene(self) -> None:
        return

    def stop_scene(self) -> None:
        return
