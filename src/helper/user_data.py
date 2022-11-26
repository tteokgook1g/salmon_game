import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from src.scene.scene_id import SceneId


@dataclass
class UserData:
    nickname: str
    scene: SceneId
    xp: int
    money: int
    level: int
    skill_point: int
    bomb_skill: bool
    lightning_skill: bool
    fullhp:float
    speed:float
    shootspeed:float

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]):
        return cls(
            dict["nickname"],
            dict["scene"],
            dict["xp"],
            dict["money"],
            dict["level"],
            dict["skill_point"],
            dict["bomb_skill"],
            dict["lightning_skill"],
            dict["fullhp"],
            dict["speed"],
            dict["shootspeed"]
        )


class UserDataFileStream:
    filepath = "./savedata.json"

    def __init__(self):
        self.data: List[UserData] = []
        self._read_from_file()

    def get_userdata(self, nickname: str) -> UserData | None:
        data = list(filter(lambda x: x.nickname == nickname, self.data))
        if not data:
            return None
        return data[-1]

    def append_userdata(self, userdata: UserData):
        self.data.append(userdata)
        self._write_on_file()

    def _read_from_file(self):
        with open(self.filepath, "r") as f:
            self.data = list(map(UserData.from_dict, (json.load(f))))

    def _write_on_file(self):
        with open(self.filepath, 'w') as f:
            json.dump(list(map(lambda x: asdict(x), self.data)), f, indent=2)
