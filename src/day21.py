from typing import Callable, Any

import numpy as np
from day16 import Node, a_star_search


def get_directional_code(password: str, keypad: dict[str, np.array], start_pos: np.array) -> set[str]:
    pos = start_pos.copy()
    vector_dir = {
        (1, 0): "v",
        (-1, 0): "^",
        (0, 1): ">",
        (0, -1): "<",
    }
    finals = [""]
    for char in password:
        char_location = keypad[char]
        vector = char_location - pos
        added1, added2 = "", ""
        for _ in range(abs(vector[0])):
            added1 += vector_dir[(int(vector[0] / abs(vector[0])), 0)]
        for _ in range(abs(vector[1])):
            added2 += vector_dir[(0, int(vector[1] / abs(vector[1])))]

        reverse = None
        if (pos + np.array([0, vector[1]]) == keypad["GAP"]).all():
            reverse = False

        if (pos + np.array([vector[0], 0]) == keypad["GAP"]).all():
            reverse = True

        pos = char_location

        if reverse is None:
            addeds = [added1 + added2 + "A", added2 + added1 + "A"]
        elif not reverse:
            addeds = [added1 + added2 + "A"]
        else:
            addeds = [added2 + added1 + "A"]

        new_finals = set()
        for final in finals:
            for added in addeds:
                new_finals.add(final + added)
        finals = set(new_finals)
    return finals


def get_nested_directional_code(password: str, num_keypad: dict[str, np.array], dir_keypad: dict[str, np.array], n_dir_layers) -> str:
    first_options = get_directional_code(password, num_keypad, num_keypad["A"])
    cache = {}

    def inner(passwords: set[str], layer: int) -> set[str]:
        print(len(passwords), layer)
        if layer == 0:
            return passwords
        next_set = set()
        for password in passwords:
            next_set.update(get_directional_code(password, dir_keypad, dir_keypad["A"]))
        return inner(next_set, layer - 1)

    bottom_options = inner(first_options, n_dir_layers)

    bottom_dict = dict(zip(map(lambda option: len(option), bottom_options), bottom_options))
    return bottom_dict[min(bottom_dict.keys())]


def get_password_sum(passwords: list[str], numpad: dict[str, np.array], dirpad: dict[str, np.array], n_layers=2):
    total = 0
    for password in passwords:
        instructions = get_nested_directional_code(password, numpad, dirpad, n_layers)
        total += len(instructions) * int(password[:-1])
    return total


if __name__ == "__main__":
    num_keypad = {
        "7": np.array([0, 0]),
        "8": np.array([0, 1]),
        "9": np.array([0, 2]),
        "4": np.array([1, 0]),
        "5": np.array([1, 1]),
        "6": np.array([1, 2]),
        "1": np.array([2, 0]),
        "2": np.array([2, 1]),
        "3": np.array([2, 2]),
        "GAP": np.array([3, 0]),
        "0": np.array([3, 1]),
        "A": np.array([3, 2]),
    }
    dir_keypad = {
        "GAP": np.array([0, 0]),
        "^": np.array([0, 1]),
        "A": np.array([0, 2]),
        "<": np.array([1, 0]),
        "v": np.array([1, 1]),
        ">": np.array([1, 2]),
    }
    passwords = []
    with open("../data/data_day21.txt", "r") as f:
        for line in f:
            if "\n" in line:
                line = line[:-1]
            passwords.append(line)
    print(passwords)
    print(get_password_sum(passwords, num_keypad, dir_keypad, 25))
