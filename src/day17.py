import time
import numpy as np


class Interpreter:

    def __init__(self, a: int, b: int, c: int):
        self.pointer = 0
        self.a: int = a
        self.b: int = b
        self.c: int = c
        self.outs = []
        self.opcode_map = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

    def combo_operand(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        if operand == 7:
            raise ValueError("7 is an invalid operand.")

    def adv(self, operand: int):
        self.a = int(self.a / (2 ** self.combo_operand(operand)))

    def bxl(self, operand: int):
        self.b = self.b ^ operand

    def bst(self, operand: int):
        self.b = self.combo_operand(operand) % 8

    def jnz(self, operand: int):
        if self.a != 0:
            self.pointer = operand - 2

    def bxc(self, operand: int):
        self.b = self.b ^ self.c

    def out(self, operand: int):
        self.outs.append(self.combo_operand(operand) % 8)

    def bdv(self, operand: int):
        self.b = int(self.a / (2 ** self.combo_operand(operand)))

    def cdv(self, operand: int):
        self.c = int(self.a / (2 ** self.combo_operand(operand)))

    def read_line(self, line: tuple[int,...]) -> tuple[int, ...]:
        while self.pointer + 1 < len(line):
            instruction = self.opcode_map[line[self.pointer]]
            operand: int = line[self.pointer + 1]
            instruction(operand)
            self.pointer += 2
        return tuple(self.outs)


def find_a(line: tuple[int,...]) -> int:
    def inner(new_line: tuple[int, ...], match_from: int) -> int:
        if len(new_line) == 0:
            return 0

        a = inner(new_line[1:], match_from + 1) * 8
        for i in range(0, 8):
            interpreted = Interpreter(a, 0, 0).read_line(line)
            if new_line == interpreted:
                return a
            a += 1

    return inner(line, 0)


if __name__ == "__main__":
    a = 266932601404433
    b = 0
    c = 0
    line = (2,4,1,3,7,5,0,3,1,4,4,7,5,5,3,0)
    interpreter = Interpreter(a, b, c)
    start_time = time.time()
    out = interpreter.read_line(line)
    print(out)