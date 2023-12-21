import random


class Actor:

    def __init__(self, name, stats, inventory):
        self.name = name
        self.stats = stats
        # TODO: inventory will contain the items and gold (list of items)
        self.inventory = inventory

    # TODO: Implement roll 20 as critial hit, fix due to new stats
    def roll_to_hit(self, hit_mod, other):
        attack_roll = random.randint(min(hit_mod, 19), 20)
        defense_roll = random.randint(min(other.defense, 19), 20)
        return (attack_roll, defense_roll)

    def combat_text(self, enemy, attack_roll, defense_roll, damage, killed):
        text = f"{self.name} rolls {attack_roll} to attack. \n {enemy.name} rolls {defense_roll} to defend."
        if damage > 0:
            text += f"\n {self.name} attacks {enemy.name}, dealing {damage} damage!"
        else:
            text += f"\n {self.name} swings at {enemy.name}, but misses!"

        return text

    def fight(self, rolls, damage, other):
        attack_roll = rolls[0]
        defense_roll = rolls[1]

        other.hp -= damage

        combat_message = self.combat_text(enemy=other,
                                          attack_roll=attack_roll,
                                          defense_roll=defense_roll,
                                          damage=damage,
                                          killed=other.hp <= 0)

        # (attack_roll, defense_roll, damage, fatal)
        return (attack_roll, defense_roll, damage, other.hp <= 0,
                combat_message)

    def melee_attack(self, other):
        # TODO: Add weapon damage if one exist
        damage = self.stats.str
        hit_mod = self.stats.str
        rolls = self.roll_to_hit(hit_mod, other)
        return self.fight(rolls, damage, other)

    # TODO: Implement ranged, magic, and other attacks
