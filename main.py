import pygame
from pygame.math import Vector2

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, WORLD_BORDER
from src.entity.abstract_entity import Transform
from src.entity.enemy import Boss
from src.entity.player import Player
from src.scene.end_scene import EndScene
from src.scene.login_scene import LoginScene
from src.scene.scene import SceneManager
from src.scene.scene_id import SceneId
from src.scene.stage1_scene import Stage1
from src.scene.stage2_scene import Stage2
from src.scene.stage3_scene import Stage3
from src.scene.start_scene import StartScene

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player_img = pygame.image.load("image/Salmon 1 big.png")
player = Player(player_img, 100, 10, Transform(
    4, Vector2(WORLD_BORDER/2, WORLD_BORDER/2), Vector2(0, 0),))
boss1_img = pygame.transform.scale(
    pygame.image.load("image/Boss 1.png"), (100, 100))
boss2_img = pygame.transform.scale(
    pygame.image.load("image/Boss 2.png"), (100, 100))
boss3_img = pygame.transform.scale(
    pygame.image.load("image/Boss 3.png"), (100, 100))
boss1 = Boss(boss1_img, 5000, 10, Transform(
    2.4, Vector2(50, 50), Vector2(0, 0)), 0)
boss2 = Boss(boss2_img, 20000, 12.5, Transform(
    3.0, Vector2(50, 50), Vector2(0, 0)), 0)
boss3 = Boss(boss3_img, 100000, 20, Transform(
    3.6, Vector2(50, 50), Vector2(0, 0)), 0)

scene_manager = SceneManager(SceneId.start_scene, screen, player)
scene_manager.add_scene(SceneId.start_scene, StartScene())
scene_manager.add_scene(SceneId.login_scene, LoginScene(player))
scene_manager.add_scene(SceneId.stage1_scene,
                        Stage1(player, boss1, scene_manager))
scene_manager.add_scene(SceneId.stage2_scene,
                        Stage2(player, boss2, scene_manager))
scene_manager.add_scene(SceneId.stage3_scene,
                        Stage3(player, boss3, scene_manager))
scene_manager.add_scene(SceneId.end_scene, EndScene(player, scene_manager))

scene_manager.run()
