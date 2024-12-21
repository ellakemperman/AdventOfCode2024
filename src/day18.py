from sys import setrecursionlimit
from typing import Callable, Any
import pandas as pd
import numpy as np
from day16 import Node, a_star_search
setrecursionlimit(10000)


class RAMNode(Node):
    move_directions = (np.array([1, 0]), np.array([-1, 0]), np.array([0, -1]), np.array([0, 1]))

    def __init__(self, cost: int, heuristic: Callable[[Node], int], position: np.array, predecessor=None):
        self.position = position
        super().__init__(cost, heuristic, predecessor)

    def create_successors(self, heuristic: Callable[[Any], int], funcs: dict[str, Callable]) -> tuple['Node',...]:
        move_is_possible = funcs["move_is_possible"]
        successors = tuple([RAMNode(self.cost + 1, heuristic, self.position + direction, predecessor=self)
                     for direction in self.move_directions if move_is_possible(self.position + direction)])
        self.successors = successors
        return successors

    def __hash__(self) -> int:
        return tuple(self.position).__hash__()

    def __str__(self) -> str:
        return "RAMNode @ " + str(self.position) + " with cost: " + str(self.cost)


def ram_search(search_space: np.ndarray, start_pos: np.array, end_pos: np.array) -> int:
    heuristic = lambda node: np.linalg.norm(node.position - end_pos)
    goal_func = lambda node: (node.position == end_pos).all()
    move_is_possible = lambda pos: ((np.array([0, 0]) <= pos).all() and (pos < search_space.shape).all()
                                    and search_space[tuple(pos)] != "#")
    start_node = RAMNode(0, heuristic, start_pos)
    end_node, _ = a_star_search(start_node, goal_func, heuristic, move_is_possible=move_is_possible)
    return len(end_node.get_predecessors())


def find_continuous_walls(data: np.ndarray, search_space: np.ndarray, find="#") -> list[np.ndarray]:
    directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1], [1, -1], [-1, -1], [1, 1], [-1, 1]])
    found = set()

    def inner(coordinates: np.ndarray) -> np.ndarray:
        # Recursive case
        found.add(tuple(coordinates))
        prev = coordinates

        for direction in directions:
            check_coords = coordinates + direction
            if (np.zeros(2) <= check_coords).all() and (check_coords < search_space.shape).all() and search_space[tuple(check_coords)] == find:
                if tuple(check_coords) not in found:
                    x = inner(check_coords)
                    prev = np.vstack((prev, x))

        return prev

    walls = []
    while data.size > 0:
        walls.append(inner(data[0]).reshape(-1, 2))
        for coords in found:
            data = data[np.logical_not(np.equal(data, coords).all(axis=1))]
        found.clear()

    return walls


def check_walls_block(wall: np.ndarray, start_pos: np.array, end_pos: np.array) -> bool:
    case1 = (wall[:, 0] == start_pos[0]).any() and (wall[:, 1] == start_pos[1]).any() # Point in wall at top edge and point in wall at left edge
    case2 = (wall[:, 0] == start_pos[0]).any() and (wall[:, 0] == end_pos[0]).any() # Point in wall at top edge and point in wall at bottom edge
    case3 = (wall[:, 0] == end_pos[0]).any() and (wall[:, 1] == end_pos[1]).any() # Point in wall at bottom edge and point in wall at right edge
    case4 = (wall[:, 1] == start_pos[1]).any() and (wall[:, 1] == end_pos[1]).any() # Point in wall at left edge and point in wall at right edge
    return case1 or case2 or case3 or case4


def find_first_complete_block_second(data: np.ndarray, search_space: np.ndarray, start_pos: np.array, end_pos: np.array, start_at=1024) -> np.array:
    for i in range(start_at, data.shape[0]):
        search_space[tuple(data[i])] = "#"
        print(i)
        walls = find_continuous_walls(data[0:i], search_space)
        blocks = tuple(filter(lambda wall: check_walls_block(wall, start_pos, end_pos), walls))
        if len(blocks) > 0:
            return data[i]
    return None


if __name__ == '__main__':
    data = pd.read_csv("../data/data_day18.csv", header=None).to_numpy()
    start = 1024
    first_kilobyte = data[0:start, :]

    space_shape = (71, 71)
    search_space = np.full(space_shape, ".")
    for coords in first_kilobyte:
        search_space[tuple(coords)] = "#"

    start_pos = np.array([0, 0])
    goal_pos = np.array([70, 70])
    print(ram_search(search_space, start_pos, goal_pos))
    print(search_space)

    print(find_first_complete_block_second(data, search_space, start_pos, goal_pos, start_at=start))
