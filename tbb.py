# Turn based battle game inspired by Pokemon
# Written by: George Dunbar (Ridonk)

import random


class Monster:
    def __init__(self, health: int, mana: int, level: int):
        self.health = health
        self.mana = mana
        self.level = level
        self._exp = 0
        self._move_list = []
        self._level_up_base = 25

    def change_health(self, amount: int):
        self.health += amount
        if self.health < 0:
            self.health = 0
            return self.health
        else:
            return self.health

    def change_mana(self, amount: int):
        self.mana += amount
        if self.mana < 0:
            self.mana = 0
            return self.mana
        else:
            return self.mana

    def _level_up(self):
        if self._exp > (self.level * self._level_up_base):
            self.level += 1
            self._level_up()

    def add_exp(self, amount: int):
        self._exp += amount
        self._level_up()

    def add_move(self, move: object) -> bool:
        if len(self._move_list) < 4:
            self._move_list.append(move)
            return True
        else:
            print("Monster already knows 4 moves!")
            return False


class Move:
    def __init__(self, lower: int, upper: int, target_other: bool):
        self.lower = lower
        self.upper = upper
        self.target_other = target_other

    def get_value_random(self):
        return random.randint(self.lower, self.upper)



