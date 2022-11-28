from typing import Generic, Iterable, Iterator, TypeVar, Union

from pygame.sprite import AbstractGroup, Sprite

T_Sprite = TypeVar("T_Sprite", bound=Sprite)


class Group(AbstractGroup, Generic[T_Sprite]):
    """한 종류의 타입을 저장하는 그룹"""

    def add(self, *sprites: Union[T_Sprite, Iterable[T_Sprite]]) -> None:  # type: ignore
        return super().add(*sprites)

    def __iter__(self) -> Iterator[T_Sprite]:
        return super().__iter__()  # type: ignore
