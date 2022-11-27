from pygame.surface import Surface
from pygame.rect import Rect
from src.entity.abstract_entity import Entity


class HealthBar():
    padding = 20

    def __init__(self, entity: Entity):
        self.entity = entity

    def update(self) -> None:
        pass

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


class BigHealthBar():
    padding = 20

    def __init__(self, entity: Entity):
        self.entity = entity

    def update(self) -> None:
        pass

    def draw(self, screen: Surface) -> None:
        bar_width, bar_height = 400, 20
        result = Surface((bar_width+2, bar_height+2))
        hp_per = self.entity.health/self.entity.fullhp
        result.fill((0, 0, 0))
        hp = Surface((abs(hp_per*bar_width), bar_height))
        if hp_per >= 0.6:
            hp.fill((0, 255, 0))
        elif hp_per >= 0.35:
            hp.fill((25500*((0.6-hp_per)*0.04), 255, 0))
        else:
            hp.fill((255, 25500*hp_per/35, 0))
        bar_rect = Rect(0, 0, bar_width+2, bar_height+2)
        bar_rect.center = 210, 18
        result.blit(hp, (1, 1))
        screen.blit(result, bar_rect)
