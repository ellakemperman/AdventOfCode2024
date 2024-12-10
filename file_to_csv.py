import re


if __name__ == "__main__":
    f_name = "test.csv"
    pattern = "[0-9]"

    with open(f_name, "r") as f:
        lines = f.readlines()

    with open(f_name, "w") as f:
        for line in lines:
            f.write(re.sub(pattern, "\g<0>,", line)[:-1])
