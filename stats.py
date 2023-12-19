class Stats():

    def __init__(self, str, agi, int, max_hp, defense):
        self.str = str
        self.agi = agi
        self.inte = int
        self.max_hp = max_hp
        self.defense = defense


class ActorStats(Stats):

    def __init__(self, str, agi, int, hp, defense, max_hp, level, exp,
                 exp_to_level):
        super().__init__(str, agi, int, max_hp, defense)
        self.level = level
        self.exp = exp
        self.exp_to_level = exp_to_level


class ItemStats(Stats):

    def __init__(self, str, agi, int, hp, defense, durability, max_durability,
                 value):
        super().__init__(str, agi, int, hp, defense)
        self.durability = durability
        self.max_durability = max_durability
        self.value = value
