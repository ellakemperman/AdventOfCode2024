import time
import numpy as np
import pandas as pd


class Board:

    def __init__(self, map: np.ndarray):
        self.map = map
        self.zeros = np.array([-1, -1])

    def check_availability(self, pos: np.array) -> bool:
        if (self.zeros < pos).all() and  (pos < self.map.shape).all() and self[pos] == "#":
            return False
        return True

    def move(self, obj: object, old_pos: np.array, new_pos: np.array) -> bool:
        self[old_pos] = obj
        if (self.zeros < new_pos).all() and  (new_pos < self.map.shape).all():
            return True
        return False

    def add_obj(self, pos: np.array, obj: object):
        if (self.zeros < pos).all() and (pos < self.map.shape).all():
            self[pos] = obj

    def __getitem__(self, item: np.array) -> object:
        return self.map[item[0], item[1]]

    def __setitem__(self, key, value) -> None:
        self.map[key[0], key[1]] = value


class Guard:

    def __init__(self, position: np.array, board: Board, direction=np.array([-1, 0])):
        self.pos = position
        self.direction = direction
        self.board = board
        # self.board.add_obj(self.pos, "X")
        self.rotation_matrix = np.array([[0, -1], [1, 0]])

    def move(self, obj="X") -> bool:
        while not self.board.check_availability(self.pos + self.direction):
            self.direction = self.direction @ self.rotation_matrix

        if self.board.move(obj, self.pos, self.pos + self.direction):
            self.pos += self.direction
            return True
        else:
            return False

    def patrol(self) -> int:
        steps = 0
        while self.move():
            steps += 1
        return steps

    def find_loops(self) -> int:
        loop_spot_counter = 0

        # For every move, if not already visited, place an object and check if it loops.
        while self.move():
            if self.board[self.pos] != "X":
                board_copy = Board(self.board.map.copy())
                board_copy.add_obj(self.pos, "#")
                sim_guard = Guard(self.pos.copy() - self.direction, board_copy, direction=self.direction.copy())
                if sim_guard.check_loop():
                    loop_spot_counter += 1
                    print(loop_spot_counter)

        return loop_spot_counter

    def check_loop(self) -> bool:
        # Loops when after a move, it arrived at a position which it had already visited and is going into the same
        # direction.
        while self.move(obj=Guard(self.pos.copy(), self.board, self.direction.copy())):
            if self == self.board[self.pos]:
                return True
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, Guard):
            return (self.pos == other.pos).all() and (self.direction == other.direction).all()
        return False


if __name__ == "__main__":
    map = pd.read_csv("data_day6.csv", header=None).to_numpy()
    guard = Guard(np.array(np.where(map == "^")).reshape(2,), Board(map))
    start_time = time.time()
    print(guard.find_loops())
    print(time.time() - start_time)

    counts = np.unique(guard.board.map, return_counts=True)
    print(counts)

