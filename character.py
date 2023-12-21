import random
import sys
from copy import deepcopy

from replit import db

from actor import Actor
import constants
from constants import GameMode
# import enemy
from enemy import Enemy
from stats import ActorStats


# Utility Functions
def str_to_class(module, classname):
    return getattr(sys.modules[module], classname)


class Character(Actor):

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
                 inventory=None,
                 mode=None,
                 battling=None,
                 user_id=None):
        if stats is not None:
            # If 'stats' is provided, use it directly
            stats = ActorStats(**stats)
        else:
            exp_to_level = level * 10
            stats = ActorStats(str, agi, int, hp, defense, max_hp, level, exp,
                               exp_to_level)
            print(stats.__dict__)
        super().__init__(name, stats, inventory)

        # TODO: Equipment system
        # Use equipped attribute on items
        self.inventory = inventory

        self.mode = mode
        if battling is not None:
            enemy_class = str_to_class(module='enemy',
                                       classname=battling["enemy"])
            self.battling = enemy_class()
            self.battling.update(**battling)
        else:
            self.battling = None
        self.user_id = user_id

    def save_to_db(self):
        character_dict = deepcopy(vars(self))
        character_dict["stats"] = self.stats.to_dict()
        if self.battling is not None:
            character_dict["battling"] = deepcopy(vars(self.battling))

        print("***", character_dict)

        db["characters"][self.user_id] = character_dict

    def hunt(self):
        # Generate random enemy to fight
        while True:
            enemy_type = random.choice(Enemy.__subclasses__())

            if enemy_type.min_level <= self.level:
                break

        enemy = enemy_type()

        # Enter battle mode
        self.mode = GameMode.BATTLE
        self.battling = enemy

        # Save changes to DB after state change
        self.save_to_db()

        return enemy

    def melee_attack(self, enemy):
        outcome = super().melee_attack(enemy)

        # Save changes to DB after state change
        self.save_to_db()

        return outcome

    def flee(self, enemy):
        if random.randint(0, 1 + self.defense):  # flee unscathed
            damage = 0
        else:  # take damage
            damage = enemy.attack / 2
            self.hp -= damage

        # Exit battle mode
        self.battling = None
        self.mode = GameMode.ADVENTURE

        # Save to DB after state change
        self.save_to_db()

        return (damage, self.hp <= 0)  #(damage, killed)

    def defeat(self, enemy):
        # no more XP after hitting level cap
        if self.level < constants.PLAYER_LVL_CAP:
            self.xp += enemy.xp

        # loot enemy
        # TODO: make a loot table and item system
        self.gold += enemy.gold

        # Exit battle mode
        self.battling = None
        self.mode = GameMode.ADVENTURE

        # Check if ready to level up after earning XP
        ready, _ = self.ready_to_level_up()

        # Save to DB after state change
        self.save_to_db()

        return (enemy.xp, enemy.gold, ready)

    def ready_to_level_up(self):
        # zero values if we've ready the level cap
        if self.stats.level == constants.PLAYER_LVL_CAP:
            return (False, 0)

        xp_needed = (self.stats.level) * 10
        return (self.stats.exp >= xp_needed, xp_needed - self.stats.exp
                )  # (ready, XP needed)

    def level_up(self, increase):
        ready, _ = self.ready_to_level_up()
        if not ready:
            return (False, self.stats.level)  # (not leveled up, current level)

        self.stats.level += 1  # increase level
        setattr(self, increase,
                getattr(self, increase) + 1)  # increase chosen stat

        self.stats.hp = self.stats.max_hp  # refill HP

        # Save to DB after state change
        self.save_to_db()

        return (True, self.stats.level)  # (leveled up, new level)

    def delete(self):
        try:
            del db["characters"][str(self.user_id)]
        except KeyError:
            print(f"Character with ID {self.user_id} not found in DB")
