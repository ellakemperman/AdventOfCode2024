import re
import numpy as np


class Robot:

    def __init__(self, line: str, max_x: int, max_y: int):
        ints = map(int, re.findall("\\d+", line))
        self.pos = np.array(ints[0:2])
        self.v = np.array(ints[2:])
        self.max = np.array([max_x, max_y])

    def step(self):
        self.pos += self.v
        min_mask = self.pos[self.pos < 0]
        max_mask = self.pos[self.pos + 1 >= self.max]
        self.pos[min_mask] = self.max - self.pos[min_mask]
        self.pos[max_mask] = self.pos[min_mask] - self.max


def simulate_bots(bots: list[Robot], n_steps: int, max_x: int, max_y: int) -> int:
    for i in range(n_steps):
        for bot in bots:
            bot.step()




if __name__ == "__main__":
    bots = []
    max_x, max_y = 101, 103

    with open("data_day14.txt", "r") as f:
        for line in f:
            bots.append(Robot(line, max_x, max_y))

    print(simulate_bots(bots, 100, max_x, max_y))
