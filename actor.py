import random


class Actor:

    def __init__(self, name, stats, inventory):
        self.name = name
        self.stats = stats
        # TODO: inventory will contain the items and gold (list of items)
        self.inventory = inventory

    # TODO: Implement roll 20 as critial hit, fix due to new stats
    def fight(self, other):
        attack_roll = random.randint(min(self.attack, 19), 20)
        defense_roll = random.randint(min(other.defense, 19), 20)
        if attack_roll > defense_roll:
            damage = self.attack
        else:
            damage = 0

        other.hp -= damage

        combat_message = self.combat_text(enemy=other,
                                          attack_roll=attack_roll,
                                          defense_roll=defense_roll,
                                          damage=damage,
                                          killed=other.hp <= 0)

        # (attack_roll, defense_roll, damage, fatal)
        return (attack_roll, defense_roll, damage, other.hp <= 0,
                combat_message)

    # FIXME
    def combat_text(self, enemy, attack_roll, defense_roll, damage, killed):
        text = f"{self.name} rolls {attack_roll} to attack. \n {enemy.name} rolls {defense_roll} to defend."
        if damage > 0:
            text += "\n {self.name} attacks {enemy.name}, dealing {damage} damage!"
        else:
            text += "\n {self.name} swings at {enemy.name}, but misses!"

        return text

    # TODO: message for killing and loot allocations
