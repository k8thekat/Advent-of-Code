import pathlib
import random
import sys

SIZE = 100
START = 50
ZERO_COUNT = 0

def brute_force_step(value: int, zero_count: int, entry: str):
    if entry[0] == "L":
        for i in range(int(entry[1:])):
            value -= 1
            if value == 0:
                zero_count += 1
            elif value < 0:
                value = SIZE - 1
    else:
        for i in range(int(entry[1:])):
            value += 1
            if value == SIZE:
                zero_count += 1
                value = 0
    return value, zero_count

with pathlib.Path(__file__).parent.joinpath("input.txt").open("r") as file:
    rotations = file.read().split("\n")

cur = START
for i in rotations:
    direction = i[:1]
    rotate = int(i[1:])
    # cur = random.randint(0, SIZE - 1)
    # rotate = random.randint(0, SIZE * 10)
    if direction.lower() == "r":  # noqa: SIM108
        result_kat = int((cur + rotate) / SIZE)
    else:
        result_kat = int((((SIZE - cur) % SIZE) + rotate) / SIZE)

    jewell_value, zero_count = brute_force_step(cur, 0, i)
    cur = jewell_value
    ZERO_COUNT += result_kat
    # zero_pass += zero_count
    # if zero_count != result_kat:
    #     print(f"cur: {cur}, rotate: {rotate}, kat: {result_kat}, jewell: {zero_count}")
    #     sys.exit(0)
    # print(f"cur: {cur}, rotate: {rotate}, kat: {result_kat}, jewell: {zero_count}")
print(ZERO_COUNT)
