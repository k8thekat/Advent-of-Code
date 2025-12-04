import pathlib

# https://adventofcode.com/2025/day/1
DIAL_START = 50
ZERO_PASS = 0
ZERO_OCCUR = 0
SIZE = 100

with pathlib.Path(__file__).parent.joinpath("input.txt").open("r") as file:
    rotations = file.read().split("\n")
print(len(rotations)) # 4424

cur = DIAL_START
for entry in rotations:
    # direction is first char of each entry.
    direction = entry[:1]
    rotate = int(entry[1:])
    print(f"Rotation Entry: {entry} | Direction: {direction} | Value: {rotate} | Current Pos/+-: {cur}")
    if direction.lower() == "r":
        pos = (cur + rotate) % SIZE
        temp = (cur + rotate) / SIZE
    else:
        pos = (cur - rotate) % SIZE
        temp = (((SIZE - cur) % SIZE) + rotate) / SIZE

    ZERO_PASS += int(temp)
    cur = pos
    if cur == 0:
        ZERO_OCCUR += 1

print("P1 -> Zero Occur", ZERO_OCCUR)
print("P2 -> Zero Passes", ZERO_PASS)

