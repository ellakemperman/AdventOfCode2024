import re


if __name__ == '__main__':
    with open("data_day3.txt", "r") as f:
        txt = ""
        for line in f:
            txt += line

        matches = re.findall("mul\\([0-9]?[0-9]?[0-9],[0-9]?[0-9]?[0-9]\\)|do\\(\\)|don't\\(\\)", txt)
        print(matches)
        total = 0
        apply = True

        for match in matches:
            if re.match("do\\(\\)", match):
                apply = True
                continue
            if re.match("don't\\(\\)", match):
                apply = False
                continue
            if apply:
                numbers = re.findall("[0-9]?[0-9]?[0-9]", match)
                total += int(numbers[0]) * int(numbers[1])

        print(total)
