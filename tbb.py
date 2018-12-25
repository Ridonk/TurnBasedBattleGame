# Turn based battle game inspired by Pokemon
# Written by: George Dunbar (Ridonk)

import random
import json


class Monster:
    def __init__(self, name: str, health: int, mana: int, level: int, speed: int, is_player: bool):
        self.name = name
        self.health = health
        self.current_health = health
        self.mana = mana
        self.level = level
        self.speed = speed
        self.is_player = is_player
        self._exp = 0
        self.move_list = []
        self._level_up_base = 25

    def change_health(self, amount: int):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0
            return self.current_health
        elif self.current_health > self.health:
            self.current_health = self.health
            return self.health
        else:
            return self.current_health

    def change_mana(self, amount: int):
        self.mana += amount
        if self.mana < 0:
            self.mana = 0
            return self.mana
        else:
            return self.mana

    def change_speed(self, amount: int):
        self.speed += amount
        if self.speed < 0:
            self.speed = 0
            return self.speed
        else:
            return self.speed

    def _level_up(self):
        if self._exp > (self.level * self._level_up_base):
            self.level += 1
            self.change_health(int(self.health * 1.25))
            self.change_mana(int(self.mana * 1.25))
            self.change_speed(int(self.speed * 1.5))
            self._level_up()

    def add_exp(self, amount: int):
        self._exp += amount
        self._level_up()

    def add_move(self, move: object) -> bool:
        if len(self.move_list) < 4:
            self.move_list.append(move)
            return True
        else:
            print("Monster already knows 4 moves!")
            return False


class Move:
    def __init__(self, name: str, lower: int, upper: int, target_other: bool, cost: int):
        self.name = name
        self.lower = lower
        self.upper = upper
        self.target_other = target_other
        self.cost = cost

    def get_value_random(self):
        return random.randint(self.lower, self.upper)


def get_int_input():
    while True:
        try:
            user_input = int(input(">>> "))
        except ValueError:
            print("Invalid selection, please try again.")
            continue
        else:
            return user_input


def load_monsters_from_config() -> list:
    monster_list = []
    with open("monsters.json", "r") as config:
        monsters_config = json.load(config)
    for monster in monsters_config["monster"]:
        monster_list.append(
            Monster(
                monster["name"],
                monster["health"],
                monster["mana"],
                monster["level"],
                monster["speed"],
                False
            ))
    for move in monsters_config["move"]:
        for monster in monster_list:
            monster.move_list.append(
                Move(
                    move["name"],
                    move["lower"],
                    move["upper"],
                    move["target"],
                    move["cost"]
                ))
    return monster_list


def battle(player: Monster, npc: Monster):
    player.is_player = True
    print("{} has {} health remaining. {} has {} health remaining".format(
        npc.name,
        npc.current_health,
        player.name,
        player.current_health))
    print("Choose a move to use from the following: ")
    i = 1
    for move in player.move_list:
        print("{}. {}".format(i, move.name))
        i += 1
    while True:
        move_key = get_int_input() - 1
        if move_key < 0 or move_key > 3:
            print("Invalid move selected, try again.")
            continue
        else:
            break
    player_move_choice = player.move_list[move_key]
    if player.speed > npc.speed:
        print("Player attacks first.")
        first = player
        second = npc
        battle_round(first, player_move_choice, second, second.move_list[0])
        # TODO: Add AI for choosing an appropriate move
    elif npc.speed > player.speed:
        print("NPC attacks first.")
        first = npc
        second = player
        battle_round(first, first.move_list[0], second, player_move_choice)
    else:
        print("Speed equal, first attacker will be random.")
        if random.randint(0, 1) == 0:
            first = player
            second = npc
            battle_round(first, player_move_choice, second, second.move_list[0])
        else:
            first = npc
            second = player
            battle_round(first, first.move_list[0], second, player_move_choice)


def battle_round(attacker: Monster, attacker_move: Move, defender: Monster, defender_move: Move):
    if attacker_move.target_other:
        attacker_damage = random.randint(attacker_move.lower, attacker_move.upper)
        defender.change_health(attacker_damage)
    else:
        attacker_damage = random.randint(attacker_move.lower, attacker_move.upper)
        attacker.change_health(attacker_damage * -1)

    if defender.current_health > 0:
        if defender_move.target_other:
            attacker_damage = random.randint(attacker_move.lower, attacker_move.upper)
            attacker.change_health(attacker_damage)
        else:
            attacker_damage = random.randint(attacker_move.lower, attacker_move.upper)
            defender.change_health(attacker_damage * -1)
    elif defender.current_health <= 0 and attacker.is_player:
        print("{} has lost! Congratulations!".format(defender.name))
        quit()
    elif defender.current_health <= 0 and not attacker.is_player:
        print("{} has lost! Better luck next time!".format(attacker.name))
        quit()

    if attacker.current_health > 0 and attacker.is_player:
        battle(attacker, defender)
    elif attacker.current_health > 0 and not attacker.is_player:
        battle(defender, attacker)
    elif attacker.current_health <= 0 and attacker.is_player:
        print("{} has lost! Better luck next time!".format(attacker.name))
        quit()
    elif attacker.current_health <= 0 and not attacker.is_player:
        print("{} has lost! Congratulations!".format(attacker.name))
        quit()


monsters = load_monsters_from_config()
battle(monsters[0], monsters[1])
