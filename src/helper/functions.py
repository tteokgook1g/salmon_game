from typing import Callable, Dict, List, Tuple, TypeVar
import pygame
from pygame.color import Color
from pygame.surface import Surface


def render_text(msg: str, color: tuple[int, int, int], font_size: int = 20, bg_color: Color | None = None) -> Surface:
    '''
    문자열 msg를 color 색깔로 render해서 return한다
    '''
    font = pygame.font.Font(None, font_size)
    return font.render(msg, True, color, bg_color)


def vector_to_tuple(vec: pygame.math.Vector2):
    return (int(vec.x), int(vec.y))


T = TypeVar("T")


def lerp(a: T, b: T, ratio: float) -> T:
    return a*(1-ratio)+b*ratio  # type: ignore


def convert_color(
        img: Surface,
        convert: Callable[[Color], Color],
) -> Surface:
    pixel = pygame.PixelArray(img)
    color_array = [[img.unmap_rgb(pixel[x, y]) for x in range(  # type: ignore
        0, img.get_width())] for y in range(0, img.get_height())]
    rgb_array = [[convert(Color(column)) for column in row]
                 for row in color_array]
    result = img.copy()
    for y, row in enumerate(rgb_array):
        for x, color in enumerate(row):
            result.set_at((x, y), color)
    return result

class Readfile:
    def read(self): 
        f = open('./save.txt', 'r')
        lst = f.readlines()[:-1]
        lst = [i.strip().split(' ') for i in lst]
        self.dic = {i[0]:tuple(eval(i[j]) for j in range(1,7)) for i in lst}
        f.close()

    def write(self, info : Dict):
        f = open('./save.txt','w')
        for i,j in info:
            s = f'{i} {j[0]} {j[1]} {j[2]} {j[3]} {j[4]} {j[5]} {j[6]}\n'
            f.write(s)
        f.close()