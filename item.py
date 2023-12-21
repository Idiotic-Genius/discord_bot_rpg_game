class Item():

    def __init__(self, name, description, stats, weight, value):
        self.name = name
        self.description = description
        self.stats = stats
        self.weight = weight
        self.value = value
        # self.broken = False    # TODO: add broken item status
        self.equipped = False

    def reduce_durabiltity(self, amount):
        self.stats.durability -= amount

    def repair(self):
        self.stats.durability = self.stats.max_durability

    def equip(self):
        self.equipped = True

    def unequip(self):
        self.equipped = False
