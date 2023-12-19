class Item():

    def __init__(self, name, description, stats, weight, value):
        self.name = name
        self.description = description
        self.stats = stats
        self.weight = weight
        self.value = value
        self.equipped = False

    def repair(self):
        self.durability = self.max_durability

    def equip(self):
        self.equipped = True

    def unequip(self):
        self.equipped = False
