class Stats():

    def __init__(self, str, agi, int, max_hp, defense):
        # TODO: Add mana and stamina stats for skills and spells
        self.str = str
        self.agi = agi
        self.int = int
        self.max_hp = max_hp
        self.defense = defense

    def to_dict(self):
        return {
            "str": self.str,
            "agi": self.agi,
            "int": self.int,
            "max_hp": self.max_hp,
            "defense": self.defense
        }


class ActorStats(Stats):

    def __init__(self, str, agi, int, hp, defense, max_hp, level, exp,
                 exp_to_level):
        super().__init__(str, agi, int, max_hp, defense)
        self.hp = hp
        self.level = level
        self.exp = exp
        self.exp_to_level = exp_to_level

    def to_dict(self):
        dict = super().to_dict()
        dict["hp"] = self.hp
        dict["level"] = self.level
        dict["exp"] = self.exp
        dict["exp_to_level"] = self.exp_to_level

        return dict


class ItemStats(Stats):

    def __init__(self, str, agi, int, hp, defense, durability, max_durability,
                 value):
        super().__init__(str, agi, int, hp, defense)
        self.durability = durability
        self.max_durability = max_durability
        self.value = value
