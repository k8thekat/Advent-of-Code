# https://adventofcode.com/2025/day/2/input

# find matching digits in number.
import pathlib

test_sample: list[str] = ["11-22","95-115","998-1012","1188511880-1188511890","222220-222224",
"1698522-1698528","446443-446449","38593856-38593862","565653-565659",
"824824821-824824827","2121212118-2121212124"]



def find_match(value: str) -> str:
    compare = ""
    half = int(len(value)/2)

    #     return ""
    for indx, _ in enumerate(value, start=1):
        # No duplicates at all
        if indx == 1 and value.find(value[0], indx) == -1:
            return ""

        # Repeating digits
        if value.count(value[0]) == len(value):
            return value

        adj_indx = indx*2

        # Too far through the value.
        if indx > half:
            # If the value is odd and our comparison is not the same length of our value (eg `99` vs `999`)
            # We fail.
            if len(value) % 2 != 0 and len(compare) != len(value):
                return ""

            return compare

        # print(f"\n{value=} | {indx=} | {adj_indx=}")
        # print(f"{value[0:indx]=} == {value[indx:adj_indx]=}")
        if value[0:indx] == value[indx:adj_indx]:
            compare = value[0:adj_indx]
            flag = False
            for m_indx in range(indx, len(value), len(compare)):
                if value[m_indx:m_indx+ len(compare)] != compare:
                    flag = True
                    break

            if flag is False:
                return value
            # res = find_match(value[indx:])
            # if res == compare:
            #     return value


        else:
            compare = ""
    return compare

with pathlib.Path(__file__).parent.joinpath("input.txt").open("r") as file:
    data = file.read().split(",")
print(len(data))


# data = test_sample
data = [entry.split("-") for entry in data]
total = 0
for entry in data:
    low, high = int(entry[0]), int(entry[1])
    data_sample = range(low, high+1)
    print(f"{low=} | {high=}")

    for digit in data_sample:
        res = find_match(str(digit))
        if len(res) >= 1:
            print(f"\n - Invalid ID: `{digit}`", "Found:", res)
            total += digit
    print(f"{total=}")
    input()



