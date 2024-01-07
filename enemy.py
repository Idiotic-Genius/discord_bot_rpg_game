import random

from actor import Actor
import constants
from stats import ActorStats


# Utility Functions
def generate_enemy_stats(min_level, max_level):
    level = random.randrange(min_level, max_level)
    str = random.randrange(constants.ENEMY_STR_MOD[0] * level,
                           constants.ENEMY_STR_MOD[1] * level)
    agi = random.randrange(constants.ENEMY_AGI_MOD[0] * level,
                           constants.ENEMY_AGI_MOD[1] * level)
    int = random.randrange(constants.ENEMY_INT_MOD[0] * level,
                           constants.ENEMY_INT_MOD[1] * level)
    max_hp = random.randrange(constants.ENEMY_MAXHP_MOD[0] * level,
                              constants.ENEMY_MAXHP_MOD[1] * level)
    defense = random.randrange(constants.ENEMY_DEFENSE_MOD[0] * level,
                               constants.ENEMY_DEFENSE_MOD[1] * level)
    exp = random.randrange(constants.ENEMY_XP_MOD[0] * level,
                           constants.ENEMY_XP_MOD[1] * level)
    # TODO: Generate loot/gold
    return ActorStats(str, agi, int, max_hp, defense, max_hp, level, exp, 0)


class Enemy(Actor):

    def __init__(self,
                 name,
                 stats=None,
                 str=None,
                 agi=None,
                 int=None,
                 hp=None,
                 defense=None,
                 max_hp=None,
                 level=None,
                 exp=None,
                 inventory=None):
        if stats is None:
            stats = ActorStats(str, agi, int, hp, defense, max_hp, level, exp,
                               0)
            super().__init__(name, stats, inventory)

    def update(self, name, stats, inventory):
        self.name = name
        self.stats = stats
        self.inventory = inventory


class GiantRat(Enemy):
    name = "🐀 Giant Rat"
    min_level = 1
    max_level = 2

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)


class GiantSpider(Enemy):
    name = "🕷️ Giant Spider"
    min_level = 1
    max_level = 2

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)


class Bat(Enemy):
    name = "🦇 Bat"
    min_level = 1
    max_level = 2

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)


class Crocodile(Enemy):
    name = "🐊 Crocodile"
    min_level = 2
    max_level = 4

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)


class Wolf(Enemy):
    name = "🐺 Wolf"
    min_level = 2
    max_level = 4

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)


class Poodle(Enemy):
    name = "🐩 Poodle"
    min_level = 3
    max_level = 5

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)


class Snake(Enemy):
    name = "🐍 Snake"
    min_level = 3
    max_level = 5

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)


class Lion(Enemy):
    name = "🦁 Lion"
    min_level = 4
    max_level = 6

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)


class Dragon(Enemy):
    name = "🐉 Dragon"
    min_level = 5
    max_level = 7

    def __init__(self):
        stats = generate_enemy_stats(min_level=self.min_level,
                                     max_level=self.max_level)
        super().__init__(name=self.name, stats=stats, inventory=None)
