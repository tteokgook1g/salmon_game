from typing import Generic, Iterable, Iterator, TypeVar, Union
from pygame.sprite import Sprite, AbstractGroup


T_Sprite = TypeVar("T_Sprite", bound=Sprite)


class Group(AbstractGroup, Generic[T_Sprite]):
    def add(self, *sprites: Union[T_Sprite, Iterable[T_Sprite]]) -> None:  # type: ignore
        return super().add(*sprites)

    def __iter__(self) -> Iterator[T_Sprite]:
        return super().__iter__()  # type: ignore
