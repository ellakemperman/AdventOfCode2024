import re
import numpy as np
from functools import reduce
from operator import mul

np.set_printoptions(threshold=np.inf, linewidth=10000)

class Robot:

    def __init__(self, line: str, max_x: int, max_y: int):
        ints = list(map(int, re.findall("-?\\d+", line)))
        self.pos = np.array(ints[0:2])
        self.v = np.array(ints[2:])
        self.max = np.array([max_x, max_y])

    def step(self):
        self.pos += self.v
        min_mask = np.where(self.pos < np.array([0, 0]))
        max_mask = np.where(self.pos >= self.max)
        self.pos[min_mask] = self.max[min_mask] + self.pos[min_mask]
        self.pos[max_mask] = self.pos[max_mask] - (self.max[max_mask])


def show_bots(bots: list[Robot], max_x: int, max_y: int) -> str:
    arr = np.zeros((max_x, max_y))
    for bot in bots:
        arr[tuple(bot.pos)] += 1

    txt = re.sub("[,\[\]. ]", "", repr(arr))[6:-1]
    return re.sub("0", ".", txt)


def simulate_bots(bots: list[Robot], n_steps: int) -> None:
    for i in range(n_steps):
        for bot in bots:
            bot.step()


def find_christmas_tree(bots: list[Robot], n_steps: int, max_x: int, max_y: int):
    for i in range(n_steps):
        simulate_bots(bots, 1)
        if i > 5000:
            txt = show_bots(bots, max_x, max_y)
            all_ns = re.findall("\\d+", txt)
            largest = reduce(lambda x, y: x if len(x) > len(y) else y, all_ns)
            if len(largest) > 10:
                print(i + 1)
                print(txt)

        if i % 100 == 0:
            print(i)


def count_bots(bots: list[Robot], n_steps: int, max_x: int, max_y: int) -> int:
    simulate_bots(bots, n_steps)

    quadrants = ((np.array([0, 0]), np.array([max_x // 2, max_y // 2])),
                 (np.array([max_x // 2 + 1, 0]), np.array([max_x, max_y // 2])),
                 (np.array([0, max_y // 2 + 1]), np.array([max_x // 2, max_y])),
                 (np.array([max_x // 2 + 1, max_y // 2 + 1]), np.array([max_x, max_y])))

    counts = [0, 0, 0, 0]
    for bot in bots:
        for i, quadrant in enumerate(quadrants):
            if (quadrant[0] <= bot.pos).all() and (bot.pos < quadrant[1]).all():
                counts[i] += 1
                continue
    return reduce(mul, counts)


if __name__ == "__main__":
    bots = []
    max_x, max_y = 101, 103

    with open("../data/data_day14.txt", "r") as f:
        for line in f:
            bots.append(Robot(line, max_x, max_y))

    # To find the christmas tree, just wait till the program prints it and its index.
    find_christmas_tree(bots, 10000, max_x, max_y)
