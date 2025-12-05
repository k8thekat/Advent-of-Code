import pathlib

# https://adventofcode.com/2025/day/3
sample = [987654321111111,811111111111119,234234234234278,818181911112111]
sample2 = [3223323232423342133321323321133325222233342332323323343713331321434231231232333333232334233323322122,
3422323123349134332433333333432333313333323413433133433343234433433334323333452433843344143323335344]

def find_highest(value: str):
    l_value, r_value = value[0],value[1]
    for entry in range(1, len(value)-1, 1):

        if value[entry] > l_value:
            l_value = value[entry]
            r_value = value[entry+1]
        elif value[entry] > r_value:
            r_value = value[entry]
    if value[-1] > r_value:
        r_value = value[-1]
    return l_value+r_value


def find_higest_x12(value: str) -> str | None:
    jolt: list[int] = list(range(12)) # We are storing the INDEXs of Value to grab numbers.
    jolt_str = ""
    last_indx = -1
    # print(f"{value=} | {len(value)=}")
    for jindx in range(0, 12, 1):
        # jindx = 0 | last_indx -1 + 1
        jolt[jindx] = last_indx + 1
        # value = 3223323232423342133321323321133325222233342332323323343713331321434231231232333333232334233323322122
        for vindx, _ in enumerate(value, last_indx+1):
            # print(f"{jolt=} | {jindx=} | {vindx=} | Math: {(len(value) - len(jolt)) + jindx:}")
            # Protects our value from going further than needed when we have less jolt values to set.
            if vindx > (len(value) - len(jolt)) + jindx:
                break

            # If the value is larger, we need to update the index in jolt.
            if value[vindx] > value[jolt[jindx]]:
                jolt[jindx] = vindx

        last_indx = jolt[jindx]
        # print(f"{last_indx=}")

    # print(jolt)
    for entry in jolt:
        # print("string", entry)
        jolt_str += value[entry]
    return jolt_str


with pathlib.Path(__file__).parent.joinpath("input.txt").open("r") as file:
    data = file.read().strip().split("\n")
print(len(data))

sample = data
total = 0
for entry in sample:
    res = find_higest_x12(str(entry))
    print(res)
    total += int(res)
print(total)
