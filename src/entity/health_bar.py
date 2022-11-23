from pygame.surface import Surface
from pygame.math import Vector2
from pygame.rect import Rect
from src.entity.abstract_entity import Entity, Transform


class HealthBar():
    padding = 20

    def __init__(self, entity: Entity):
        self.entity = entity
        self.transform = Transform(
            0, self.entity.transform.pos-Vector2(0, 40), Vector2(1, 0))

    def update(self) -> None:
        self.transform = Transform(
            0, self.entity.transform.pos-Vector2(0, 40), Vector2(1, 0))

    def draw(self, screen: Surface) -> None:
        bar_width, bar_height = 60, 10
        result = Surface((bar_width+2, bar_height+2))
        hp_per = self.entity.health/self.entity.fullhp
        result.fill((0, 0, 0))
        hp = Surface((abs(hp_per*bar_width), bar_height))
        if hp_per <= 0.3:
            hp.fill((255, 0, 0))
        else:
            hp.fill((0, 255, 0))
        bar_rect = Rect(0, 0, bar_width+2, bar_height+2)
        bar_rect.midbottom = self.entity.rect.centerx, (
            self.entity.rect.top-self.padding)
        result.blit(hp, (1, 1))
        screen.blit(result, bar_rect)
