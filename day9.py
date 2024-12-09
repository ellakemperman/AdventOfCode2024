import numpy as np
import time


class Disk:

    def __init__(self, disk_str: str):
        self.data = []
        self.empty_pointer = 0

        for i, char in enumerate(disk_str):
            if i % 2 == 0:
                i_d = int(i / 2)
            else:
                i_d = -1

            for _ in range(int(char)):
                self.data.append(i_d)

    def compact_disk_fully(self):
        while self.__advance_pointer():
            next_move = self.data.pop()
            if next_move != -1:
                self.data[self.empty_pointer] = next_move

    def compact_disk_efficient(self):
        i_d = self.data[-1]
        count = 0
        i = len(self.data) - 1
        while i > self.empty_pointer:
            if self.data[i] != i_d:
                if i_d != -1 and self.attempt_move(i_d, count, i + 1):
                    self.data[i + 1 : i + count + 1] = [-1 for i in range(count)]
                i_d = self.data[i]
                count = 0
            i -= 1
            count += 1

    def attempt_move(self, i_d: int, count: int, max_index: int):
        search_obj = [-1 for _ in range(count)]

        for i in range(self.empty_pointer, max_index):
            if self.data[i : i + count] == search_obj:
                self.data[i : i + count] = [i_d for _ in range(i, i + count)]
                self.__advance_pointer()
                return True
        return False

    def __advance_pointer(self):
        try:
            while self.data[self.empty_pointer] != -1:
                self.empty_pointer += 1
            return True
        except IndexError:
            return False

    def check_sum(self):
        checksum = 0
        for i, i_d in enumerate(self.data):
            if i_d != -1:
                checksum += i * i_d
        return checksum

    def __str__(self):
        str_repr = ""
        for point in self.data:
            if point == -1:
                str_repr += "."
            else:
                str_repr += str(point)
        return str_repr


if __name__ == "__main__":
    with open("data_day9.txt", "r") as f:
        disk_str = f.readline()

    disk = Disk(disk_str)

    start_time = time.time()
    disk.compact_disk_efficient()
    print(f"Time elapsed: {(time.time() - start_time).__round__(5)} s")

    print(f"Final sum: {disk.check_sum()}")
