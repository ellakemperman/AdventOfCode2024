from typing import Callable


def mul(x: int, y: int) -> int:
    return x * y


def add(x: int, y: int) -> int:
    return x + y


def concat(x: int, y: int) -> int:
    return int(str(x) + str(y))


def check_line(total: int, numbers: list[int], operators: tuple[Callable[[int, int], int]]) -> bool:

    def inner(numbers) -> list[int]:
        if len(numbers) == 2:
            lst = []
            for operator in operators:
                lst.append(operator(numbers[0], numbers[1]))
            return lst

        previous = inner(numbers[:len(numbers) - 1])
        new = []
        for n in previous:
            for operator in operators:
                new.append(operator(n, numbers[-1]))
        return new
    return total in inner(numbers)


def count_calibration(data: list[tuple], operators=(add, mul)) -> int:
    return sum(map(lambda x: x[0], filter(lambda x: check_line(x[0], x[1], operators), data)))


if __name__ == "__main__":
    data = []
    with open("data_day7.txt", "r") as f:
        for line in f:
            line_str = line.split(":")
            total = int(line_str[0])
            numbers_str = line_str[1].split(" ")
            numbers = []
            for number in numbers_str:
                numbers.append(int(number))

            data.append((total, numbers))

    print(count_calibration(data, (mul, add, concat)))