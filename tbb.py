# Turn based battle game inspired by Pokemon
# Written by: George Dunbar (Ridonk)

import random
import json


class Monster:
    def __init__(self, name: str, health: int, mana: int, level: int):
        self.name = name
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
            self.change_health(int(self.health * 1.25))
            self.change_mana(int(self.mana * 1.25))
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


def load_monsters_from_config():
    monster_list = []
    with open("monsters.json", "r") as config:
        monsters_config = json.load(config)
    for monster in monsters_config["monster"]:
        monster_list.append(
            Monster(monster["name"],
                    monster["health"],
                    monster["mana"],
                    monster["level"]))

