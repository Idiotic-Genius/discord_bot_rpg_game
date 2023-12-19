class Item():
    def __init__(self, name, description, stats, weight, value):
        self.name = name
        self.description = description
        self.stats = stats  # TODO: 
        self.weight = weight
        self.value = value
        self.equipped = False