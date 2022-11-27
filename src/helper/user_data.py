import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from src.scene.scene_id import SceneId


@dataclass
class UserData:
    """저장할 플레이어 데이터"""
    nickname: str
    scene: SceneId
    xp: int
    money: int
    level: int
    skill_point: int
    bomb_skill: bool
    lightning_skill: bool
    fullhp: float
    speed: float
    shootspeed: float

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
    """플레이어 데이터를 JSON 형식으로 저장"""
    filepath = "./savedata.json"

    def __init__(self):
        self.data: List[UserData] = []
        self._read_from_file()

    def get_userdata(self, nickname: str) -> UserData | None:
        """해당 닉네임의 가장 마지막 플레이의 데이터를 불러옴"""
        data = list(filter(lambda x: x.nickname == nickname, self.data))
        if not data:
            return None
        return data[-1]

    def append_userdata(self, userdata: UserData):
        """저장할 데이터를 맨 뒤에 추가함"""
        self.data.append(userdata)
        self._write_on_file()

    def _read_from_file(self):
        with open(self.filepath, "r") as f:
            self.data = list(map(UserData.from_dict, (json.load(f))))

    def _write_on_file(self):
        with open(self.filepath, 'w') as f:
            json.dump(list(map(lambda x: asdict(x), self.data)), f, indent=2)
