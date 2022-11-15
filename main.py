import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.scene.login_scene import LoginScene
from src.scene.scene import SceneManager
from src.scene.scene_id import SceneId
from src.scene.start_scene import StartScene

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

scene_manager = SceneManager(SceneId.start_scene)
scene_manager.add_scene(SceneId.start_scene, StartScene())
scene_manager.add_scene(SceneId.login_scene, LoginScene())

pygame.init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key_pressed = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    scene_manager.update(key_pressed, mouse_pos,mouse_click)

    scene_manager.draw(screen)

    pygame.display.update()
