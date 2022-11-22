"""dataclass for parameter of the methods "update" """

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Sequence, Tuple

if TYPE_CHECKING:
    from pygame.event import Event
    from src.entity.player import Player


@dataclass
class UpdateInfo:
    __slots__ = ("key_pressed", "mouse_pos", "mouse_click",
                 "events", "player", "is_paused")
    key_pressed: Sequence[bool]
    mouse_pos: Tuple[int, int]
    mouse_click: Tuple[int, int, int]
    events: List[Event]
    player: Player | None
    is_paused: bool
