# Turn based battle game inspired by Pokemon
# Written by: George Dunbar (Ridonk)

import random


class Monster:
    def __init__(self, health: int, mana: int, level: int):
        self.health = health
        self.mana = mana
        self.level = level
        self.exp = 0
        self.move_list = []


class Move:
    def __init__(self, lower: int, upper: int, target_other: bool):
        self.lower = lower
        self.upper = upper
        self.target_other = target_other

    def get_value_random(self):
        return random.randint(self.lower, self.upper)



