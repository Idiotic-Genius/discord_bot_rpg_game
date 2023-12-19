import random


class Actor:

    def __init__(self, name, hp, max_hp, attack, defense, xp, gold):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.xp = xp
        self.gold = gold

    # TODO: Implement roll 20 as critial hit
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

    def combat_text(self, enemy, attack_roll, defense_roll, damage, killed):
        text = f"{self.name} rolls {attack_roll} to attack. \n {enemy.name} rolls {defense_roll} to defend."
        if damage > 0:
            text += "\n {self.name} attacks {enemy.name}, dealing {damage} damage!"
        else:
            text += "\n {self.name} swings at {enemy.name}, but misses!"

        return text

    # TODO: message for killing and loot allocations
