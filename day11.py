from abc import abstractmethod
from typing import Callable, Sequence


class StoneRule:

    @staticmethod
    @abstractmethod
    def check_applicable(stone: int) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def apply(stone: int) -> tuple[int, ...]:
        pass


class ZeroToOneRule(StoneRule):

    @staticmethod
    def check_applicable(stone: int) -> bool:
        return stone == 0

    @staticmethod
    def apply(stone: int) -> tuple[int, ...]:
        return (1,)


class StoneSplitRule(StoneRule):

    @staticmethod
    def check_applicable(stone: int) -> bool:
        return len(str(stone)) % 2 == 0

    @staticmethod
    def apply(stone: int) -> tuple[int, ...]:
        str_stone = str(stone)
        return int(str_stone[0:len(str_stone) // 2]), int(str_stone[len(str_stone) // 2:])


class DefaultRule(StoneRule):

    @staticmethod
    def check_applicable(stone: int) -> bool:
        return True

    @staticmethod
    def apply(stone: int) -> tuple[int, ...]:
        return (stone * 2024,)


def apply_rules(stone: int, rules: tuple[StoneRule, ...]) -> tuple[int, ...]:
    for rule in rules:
        if rule.check_applicable(stone):
            return rule.apply(stone)


def map_stones(func: Callable[[int], Sequence[int]], xs: dict[int, int]) -> dict[int, int]:
    stone_dict = {}
    for key, val in xs.items():
        mapped = func(key)
        for ele in mapped:
            try:
                stone_dict[ele] += val
            except KeyError:
                stone_dict[ele] = val

    return stone_dict


def simulate_stone(stones: dict[int, int], rules: tuple[StoneRule, ...], n_sims: int) -> dict[int, int]:
    prev = 1
    for i in range(n_sims):
        stones = map_stones(lambda stone: apply_rules(stone, rules), stones)
        length = len(stones)
        print(length / prev)
        prev = length

    return stones


if __name__ == '__main__':
    rules = (ZeroToOneRule(), StoneSplitRule(), DefaultRule())
    with open("day11.txt", "r") as f:
        line = f.readline()
    data = {}
    for ele in line.split(" "):
        try:
            data[int(ele)] += 1
        except KeyError:
            data[int(ele)] = 1

    print(sum(simulate_stone(data, rules, 75).values()))

"""
def flatmap[T,U](func: Callable[[T], Sequence[U]], xs: Sequence[T]) -> Sequence[U]:
    mapped = list(map(func, xs))
    final = []
    for x in mapped:
        final.extend(x)
    return final
"""
