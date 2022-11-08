from typing import Generic, Iterable, Iterator, TypeVar, Union
from pygame.sprite import Sprite, AbstractGroup


T = TypeVar("T", bound=Sprite)


class Group(AbstractGroup, Generic[T]):
    def add(self, *sprites: Union[T, Iterable[T]]) -> None:  # type: ignore
        return super().add(*sprites)

    def __iter__(self) -> Iterator[T]:
        return super().__iter__()  # type: ignore
