import random

from actor import Actor
import constants


# Utility Functions
def generate_enemy_attributes(name, min_level, max_level):
    level = random.randrange(min_level, max_level)
    max_hp = random.randrange(constants.ENEMY_HP_MOD[0] * level,
                              constants.ENEMY_HP_MOD[1] * level)
    attack = random.randrange(constants.ENEMY_ATTACK_MOD[0] * level,
                              constants.ENEMY_ATTACK_MOD[1] * level)
    defense = random.randrange(constants.ENEMY_DEFENSE_MOD[0] * level,
                               constants.ENEMY_DEFENSE_MOD[1] * level)
    mana = 0
    xp = random.randrange(constants.ENEMY_XP_MOD[0] * level,
                          constants.ENEMY_XP_MOD[1] * level)
    gold = random.randrange(constants.ENEMY_GOLD_MOD[0] * level,
                            constants.ENEMY_GOLD_MOD[1] * level)

    return {
        "name": name,
        "level": level,
        "max_hp": max_hp,
        "attack": attack,
        "defense": defense,
        "mana": mana,
        "level": level,
        "xp": xp,
        "gold": gold
    }


class Enemy(Actor):

    def __init__(self, name, max_hp, attack, defense, mana, level, xp, gold):
        super().__init__(name=name,
                         hp=max_hp,
                         max_hp=max_hp,
                         attack=attack,
                         defense=defense,
                         xp=xp,
                         gold=gold)
        self.enemy = self.__class__.__name__
        self.mana = mana
        self.level = level

    def update(self, name, hp, max_hp, attack, defense, mana, level, xp, gold,
               enemy):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.mana = mana
        self.level = level
        self.xp = xp
        self.gold = gold


class GiantRat(Enemy):
    name = "🐀 Giant Rat"
    min_level = 1
    max_level = 2

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)


class GiantSpider(Enemy):
    name = "🕷️ Giant Spider"
    min_level = 1
    max_level = 2

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)


class Bat(Enemy):
    name = "🦇 Bat"
    min_level = 1
    max_level = 2

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)


class Crocodile(Enemy):
    name = "🐊 Crocodile"
    min_level = 2
    max_level = 4

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)


class Wolf(Enemy):
    name = "🐺 Wolf"
    min_level = 2
    max_level = 4

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)


class Poodle(Enemy):
    name = "🐩 Poodle"
    min_level = 3
    max_level = 5

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)


class Snake(Enemy):
    name = "🐍 Snake"
    min_level = 3
    max_level = 5

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)


class Lion(Enemy):
    name = "🦁 Lion"
    min_level = 4
    max_level = 6

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)


class Dragon(Enemy):
    name = "🐉 Dragon"
    min_level = 5
    max_level = 7

    def __init__(self):
        attributes = generate_enemy_attributes(name=self.name,
                                               min_level=self.min_level,
                                               max_level=self.max_level)
        super().__init__(**attributes)
