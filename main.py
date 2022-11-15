import pygame
from pygame.math import Vector2
from pygame.surface import Surface

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entity.abstract_entity import Transform
from src.entity.player import Player
from src.scene.login_scene import LoginScene
from src.scene.scene import SceneManager
from src.scene.scene_id import SceneId
from src.scene.stage_camera_test import StageCameraTest
from src.scene.start_scene import StartScene

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player_img = Surface((50, 50))
player_img.fill((200, 100, 0))
player = Player(player_img, 100, 10, Transform(
    1, Vector2(100, 100), Vector2(0, 0)))

scene_manager = SceneManager(SceneId.start_scene, screen)
scene_manager.add_scene(SceneId.start_scene, StartScene())
scene_manager.add_scene(SceneId.login_scene, LoginScene())
scene_manager.add_scene(SceneId.stage_camera_test, StageCameraTest(player))

scene_manager.run()
