"""defines SceneId. you must add id when you add a new scene."""


from enum import Enum, auto


class SceneId(Enum):
    main_scene = auto()
    start_scene = auto()
    login_scene = auto()
    stage1_scene = auto()
    stage2_scene = auto()
    stage3_scene = auto()
    end_scene = auto()