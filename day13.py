import re
import numpy as np


def solve_claw_machine(claw_machine: tuple[np.ndarray, np.array], a_cost: int, b_cost: int,
                       check_less_than=np.array([100, 100])) -> int:

    solution = np.around(np.linalg.solve(claw_machine[0].T, claw_machine[1]), decimals=4)
    if (solution.astype(int) == solution).all() and (solution >= np.array([0, 0])).all() and (solution <= check_less_than).all():
        return a_cost * int(solution[0]) + b_cost * int(solution[1])
    return 0


def solve_all_claw_machines(claw_machines: list[tuple[np.ndarray, np.array]], a_cost=3, b_cost=1) -> int:
    return sum(map(lambda x: solve_claw_machine(x, a_cost, b_cost), claw_machines))


def solve_all_greater_claw_machines(claw_machines: list[tuple[np.ndarray, np.array]], a_cost=3, b_cost=1,
                                    prize_offset=10000000000000) -> int:

    return sum(map(lambda x: solve_claw_machine((x[0], x[1] + prize_offset), a_cost, b_cost,
                                                check_less_than=np.array([np.inf, np.inf])), claw_machines))


def parse_line(line: str) -> list[int]:
    return list(map(int, re.findall("\\d+", line)))


if __name__ == "__main__":
    claw_machines = []
    with open("data_day13.txt", "r") as f:
        a = []
        b = []
        target = []
        for i, line in enumerate(f):
            if i % 4 == 0:
                a = parse_line(line)
            elif i % 4 == 1:
                b = parse_line(line)
            elif i % 4 == 2:
                matrix = np.array([a, b])
                target = np.array(parse_line(line))
                claw_machines.append((matrix, target))


    print(solve_all_greater_claw_machines(claw_machines))