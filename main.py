import pygame
from pygame.math import Vector2

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entity.abstract_entity import Transform
from src.entity.player import Player
from src.entity.enemy import Boss
from src.scene.login_scene import LoginScene
from src.scene.scene import SceneManager
from src.scene.scene_id import SceneId
from src.scene.stage1_scene import Stage1
from src.scene.stage1_to_2_scene import Stage1to2
from src.scene.stage2_scene import Stage2
from src.scene.start_scene import StartScene
from src.scene.end_scene import EndScene

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player_img = pygame.image.load("image/Salmon 1.png")
player = Player(player_img, 100, 10, Transform(
    3, Vector2(200, 100), Vector2(0, 0),), (0, 0, 0, []))
boss_img = pygame.image.load("image/Boss.png")
boss = Boss(boss_img, 20, 20, Transform(
    2.5, Vector2(50, 50), Vector2(0, 0)))

scene_manager = SceneManager(SceneId.start_scene, screen)
scene_manager.add_scene(SceneId.start_scene, StartScene())
scene_manager.add_scene(SceneId.login_scene, LoginScene())
scene_manager.add_scene(SceneId.stage1_scene, Stage1(player, boss))
scene_manager.add_scene(SceneId.stage1to2_scene,
                        Stage1to2(player, scene_manager))
scene_manager.add_scene(SceneId.stage2_scene, Stage2(player, boss))
scene_manager.add_scene(SceneId.end_scene, EndScene(player, scene_manager))

scene_manager.run()
