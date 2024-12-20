from queue import PriorityQueue
import numpy as np
from typing import Callable
import pandas as pd
import time
np.set_printoptions(threshold=np.inf, linewidth=10000)


class Node:
    forward_cost = 1
    turn_cost = 1000
    turn_direction_cw = np.array([[0, 1], [-1, 0]])
    turn_direction_ccw = np.array([[0, -1], [1, 0]])

    def __init__(self, position: np.array, direction: np.array, cost: int, eval: int, predecessor=None):
        self.pos = position
        self.dir = direction
        self.cost = cost
        self.val = eval + cost
        self.predecessor = predecessor

    def get_successor(self, heuristic: Callable[[np.array], int], move_is_possible: Callable[[np.array], bool]) -> tuple['Node',...]:
        new_pos = self.pos + self.dir
        successor2 = Node(self.pos, self.dir @ self.turn_direction_cw, self.cost + self.turn_cost, heuristic(self.pos), predecessor=self)
        successor3 = Node(self.pos, self.dir @ self.turn_direction_ccw, self.cost + self.turn_cost, heuristic(self.pos), predecessor=self)
        if move_is_possible(new_pos):
            successor1 = Node(new_pos, self.dir, self.cost + self.forward_cost, heuristic(new_pos), predecessor=self)
            return successor1, successor2, successor3

        return successor2, successor3

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.val < other.val
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Node):
            return self.val > other.val
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Node):
            return (self.dir == other.dir).all() and (self.pos == other.pos).all()
        return False

    def __str__(self) -> str:
        return "Node @ " + str(self.pos) + " with value " + str(self.val)

    def __hash__(self):
        return (tuple(self.pos), tuple(self.dir)).__hash__()

    def get_predecessors(self) -> list['Node']:
        try:
            return [self] + self.predecessor.get_predecessors()
        except AttributeError:
            return []

    def cost_eq(self, other: 'Node') -> bool:
        return self.cost == other.cost


def a_star_search(search_space: np.ndarray, start_pos: np.array, start_direction: np.array, goal_pos: np.array) -> tuple[Node, set[Node]]:
    queue = PriorityQueue()
    heuristic = lambda pos: np.linalg.norm(pos - goal_pos)
    move_is_possible = lambda pos: search_space[tuple(pos)] != "#"
    queue.put(Node(start_pos, start_direction, 0, heuristic(start_pos)))

    seen_nodes = set()

    while queue.not_empty:
        next_node: Node = queue.get()
        seen_nodes.add(next_node)
        if (next_node.pos == goal_pos).all():
            return next_node, seen_nodes

        for node in next_node.get_successor(heuristic, move_is_possible):
            if node not in seen_nodes:

                queue.put(node)


def get_all_paths(search_space: np.ndarray, start_pos: np.array, start_direction: np.array, goal_pos: np.array) -> int:
    end_node, seen_nodes = a_star_search(search_space, start_pos, start_direction, goal_pos)
    best_path = end_node.get_predecessors()
    nodes_on_path = set(map(lambda node: (tuple(node.pos), node.cost), best_path))

    heuristic = lambda pos: 0
    move_is_possible = lambda pos: search_space[tuple(pos)] != "#"

    for node in seen_nodes:
        if node in nodes_on_path:
            continue

        successors = node.get_successor(heuristic, move_is_possible)
        for successor in successors:
            pos = (tuple(successor.pos), successor.cost)

            if pos in nodes_on_path:
                for predecessor in node.get_predecessors():
                    nodes_on_path.add((tuple(predecessor.pos), predecessor.cost))
                break

    for node, _ in nodes_on_path:
        search_space[node] = "O"

    print(search_space)

    nodes_on_path = set(map(lambda node: node[0], nodes_on_path))
    return len(nodes_on_path)


if __name__ == '__main__':
    search_space = pd.read_csv("../data/data_day16.csv", header=None).to_numpy()
    start_pos = np.array(np.where(search_space == "S")).reshape(2,)
    goal_pos = np.array(np.where(search_space == "E")).reshape(2,)
    start_direction = np.array([0, 1])

    start_time = time.time()
    print(get_all_paths(search_space, start_pos, start_direction, goal_pos))
    print(time.time() - start_time)
    print(np.unique(search_space, return_counts=True))