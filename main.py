import pygame

from src.scene.scene import SceneManager
from src.scene.scene_id import SceneId
from src.scene.start_scene import StartScene

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

scene_manager = SceneManager(SceneId.start_scene)
scene_manager.add_scene(SceneId.start_scene, StartScene())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key_pressed = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    scene_manager.update(key_pressed, mouse_pos)

    scene_manager.draw(screen)

    pygame.display.update()
