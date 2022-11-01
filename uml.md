::: mermaid
classDiagram

class Stage
Stage*--Entity

class Transform{
    +pygame.Vector2 pos
    +float velocity
    +pygame.Vector2 direction

    +move() None
    +towards(pygame.Vector2 pos) None
    +away_from(pygame.Vector2 pos) None
}


class Entity{
    +float hp
    +Transform transform

    +update(key, mouse) None
}

class Sprite{
    +Rect rect
    +pygame.Surface image

    +update() None
}
Sprite<--Entity

class Enemy

class Player{
    +int xp
    +int money
}


Entity<--Enemy
Entity<--Player


class Reward{
    +int xp
    +int money
}
Entity<--Reward
Enemy--Reward


class SkillParticle
class Skill{
    +static Group particleGroup # ref
    +makeParticle()
}
Entity<--SkillParticle
Skill--SkillParticle
Player--Skill

:::