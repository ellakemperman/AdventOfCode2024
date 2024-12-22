from sys import setrecursionlimit
import numpy as np
import pandas as pd
np.set_printoptions(threshold=np.inf, linewidth=10000)


def number_tiles(data: np.ndarray, start_pos: np.array, goal_pos: np.array) -> np.ndarray:
    directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    pos = start_pos.copy()
    i = 0
    copy_data = data.copy()
    copy_data[tuple(goal_pos)] = "."

    while not (pos == goal_pos).all():
        copy_data[tuple(pos)] = i
        i += 1
        for direction in directions:
            if copy_data[tuple(pos + direction)] == ".":
                pos += direction
                break

    copy_data[tuple(goal_pos)] = i
    return copy_data


def get_cheat_range_vectors(directions: np.ndarray, max_range: int) -> list[np.array]:
    def inner(range: int, vectors: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]]:
        if range == 0:
            return vectors

        new = vectors.copy()
        for direction in directions:
            for vector in vectors:
                new = new.union([tuple(np.array(vector) + direction)])

        return inner(range - 1, new)

    return list(map(lambda ele: np.array(ele), inner(max_range, frozenset([tuple(np.array([0, 0]))]))))



def find_all_gt_differentials(data: np.ndarray, start_pos: np.array, goal_pos: np.array, min_differential: int, max_range: int) -> int:
    directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    cheat_vectors = get_cheat_range_vectors(directions, max_range)
    pos = start_pos
    i = 0
    good_cheat_counter = 0
    while not (pos == goal_pos).all():
        print(data[tuple(pos)])

        # Find all good cheats
        for vector in cheat_vectors:
            new_pos = pos + vector
            if (np.array([0, 0]) <= new_pos).all() and (new_pos < data.shape).all():
                ele = data[tuple(new_pos)]
                if isinstance(ele, int) and ele - i >= min_differential + np.sum(np.abs(vector)):
                    good_cheat_counter += 1

        # Pos update
        for direction in directions:
            next_space = data[tuple(pos + direction)]
            if isinstance(next_space, int) and next_space > i:
                pos += direction
                i += 1
                break

    return good_cheat_counter


if __name__ == "__main__":
    data = pd.read_csv("../data/data_day20.csv", header=None).to_numpy()
    start_pos = np.array(np.where(data == "S")).reshape(2,)
    goal_pos = np.array(np.where(data == "E")).reshape(2,)
    max_cheat_second = 20

    edited_data = number_tiles(data, start_pos, goal_pos)
    # print(edited_data)
    print("Final output:", find_all_gt_differentials(edited_data, start_pos, goal_pos, 100, max_cheat_second))

