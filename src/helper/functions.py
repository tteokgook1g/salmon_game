import pygame
from pygame.color import Color
from pygame.surface import Surface


def render_text(msg: str, color: tuple[int, int, int], font_size: int = 20, bg_color: Color | None = None) -> Surface:
    '''
    문자열 msg를 color 색깔로 render해서 return한다
    '''
    font = pygame.font.Font(None, font_size)
    return font.render(msg, True, color, bg_color)
