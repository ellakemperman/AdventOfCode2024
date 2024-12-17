import pandas as pd
import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=10000)


def move(ocean: np.ndarray, robot_pos: np.array, direction: np.array) -> np.array:
    next_pos = robot_pos + direction
    next_ele = ocean[tuple(next_pos)]
    if next_ele == "." or ((next_ele == "O" or next_ele == "[" or next_ele == "]") and try_move_crates(ocean, next_pos, direction)):
        ocean[tuple(next_pos)] = "@"
        ocean[tuple(robot_pos)] = "."
        return robot_pos + direction

    return robot_pos


def try_move_crates(ocean: np.ndarray, crate_pos: np.array, direction: np.array) -> bool:
    def inner(crate_pos: np.array, do_move=False, check_back=True):
        next_pos = crate_pos + direction
        ele = ocean[tuple(crate_pos)]
        if ele == ".":
            return True
        elif ele == "#":
            return False

        if inner(next_pos, do_move=do_move):
            neighbour = True
            if ((direction == np.array([-1, 0])).all() or (direction == np.array([1, 0])).all()) and check_back:
                if ele == "[":
                    neighbour = inner(crate_pos + np.array([0, 1]), do_move=do_move, check_back=False)
                elif ele == "]":
                    neighbour = inner(crate_pos + np.array([0, -1]), do_move=do_move, check_back=False)

            if do_move:
                ocean[tuple(next_pos)] = ocean[tuple(crate_pos)]
                ocean[tuple(crate_pos)] = "."

            return neighbour

        return False

    if inner(crate_pos):
        return inner(crate_pos, do_move=True)
    return False


def simulate_robot(ocean: np.ndarray, robot_pos: np.array, directions: list[np.array]) -> np.ndarray:
    for direction in directions:
        robot_pos = move(ocean, robot_pos, direction)
    return ocean


def score_ocean(ocean: np.ndarray, target: str) -> int:
    locations = np.array(np.where(ocean == target)).T
    return sum(map(lambda loc: loc[0] * 100 + loc[1], locations))


def scale_ocean(ocean: np.ndarray) -> np.ndarray:
    new_ocean = []
    for row in ocean:
        new_row = []
        for ele in row:
            match ele:
                case ".": new_row.extend([".", "."])
                case "#": new_row.extend(["#", "#"])
                case "O": new_row.extend(["[", "]"])
                case "@": new_row.extend(["@", "."])
        new_ocean.append(np.array(new_row))

    return np.array(new_ocean)


if __name__ == "__main__":
    ocean = pd.read_csv("data_day15.csv", header=None).to_numpy()
    extended_ocean = scale_ocean(ocean)

    with open("data_day15.txt", "r") as f:
        instructions_str = f.readline()
        instructions = []

        for instruction in instructions_str:
            match instruction:
                case "^": instructions.append(np.array([-1, 0]))
                case ">": instructions.append(np.array([0, 1]))
                case "v": instructions.append(np.array([1, 0]))
                case "<": instructions.append(np.array([0, -1]))

    # robot_pos = np.array(np.where(ocean == "@")).reshape(2,)
    # ocean = simulate_robot(ocean, robot_pos, instructions)

    # print(score_ocean(ocean, "O"))

    robot_extended_pos = np.array(np.where(extended_ocean == "@")).reshape(2,)
    extended_ocean = simulate_robot(extended_ocean, robot_extended_pos, instructions)

    print(score_ocean(extended_ocean, "["))
