# https://adventofcode.com/2025/day/4

# @
import pathlib

with pathlib.Path(__file__).parent.joinpath("input.txt").open("r") as file:
    data = file.read().strip()
print(len(data))

sample = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


def format_data(value: str):
    data: list[str] = value.split("\n")
    for indx, entry in enumerate(data, 0):
        data[indx] = list("." + entry + ".")
    line_length = len(data[0])
    data.insert(0, list(line_length*"."))
    data.append(list(line_length*"."))
    return data

def find_symbol(value: list[str], x_indx: int, y_indx: int) -> int:
    """Returns 1 if less than 4 `@` symbols found."""
    counter = 0
    for entry in range(-1, 2):
        row = value[y_indx + entry]
        if row[x_indx-1] == "@":
            counter += 1
        if row[x_indx+1] == "@":
            counter += 1
        if entry != 0 and row[x_indx] == "@":
            counter += 1

    return int(counter < 4)

def parse_data(data: list[str]) -> bool:
    global ROLLS  # noqa: PLW0603
    flag = False
    for yindx in range(1, len(data)-1):
        for xindx in range(1, len(data[yindx])-1):
            if data[yindx][xindx] == "@":
                rolls = find_symbol(data, xindx, yindx)
                if rolls == 1:
                    ROLLS+= 1
                    data[yindx][xindx] = "."
                    flag = True
    return flag

data = format_data(data)
ROLLS = 0
while(parse_data(data)):
    print(ROLLS)

