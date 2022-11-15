"""defines SceneId. you must add id when you add a new scene."""


from enum import Enum, auto


class SceneId(Enum):
    main_scene = auto()
    start_scene = auto()
    login_scene = auto()
    stage_camera_test = auto()
