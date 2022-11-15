from pygame import Vector2
from src.entity.abstract_entity import Enemy, Transform
from src.scene.scene import Stage
from src.scene.scene_id import SceneId
from pygame.surface import Surface


class StageCameraTest(Stage):
    def check_scene_switch(self) -> SceneId | None:
        return None

    def start_scene(self) -> None:
        enemy_img = Surface((30, 30))
        enemy_img.fill((0, 200, 0))
        self.enemies.add(Enemy(enemy_img, 1, 1, Transform(
            0, Vector2(50, 50), Vector2(0, 1))))
        return

    def stop_scene(self) -> None:
        return
