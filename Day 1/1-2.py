from input import text as text_input


def format_text(text: str):
    res: list[str] = text.split("\n")
    return res


def grab_num(text: list[str]):
    nums: list = [str(x) for x in range(0, 10, 1)]
    word_nums: list = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    # word_nums: list = ["nine", "eight", "seven", "six", "five", "four", "three", "two", "one"]
    num = 0

    for string in text:
        first_value = None
        second_value = None
        temp_str = ""
        for char in string:
            temp_str += char
            if char in nums:
                temp_str = ""
                if first_value == None:
                    first_value = char
                else:
                    second_value = char
            else:
                for word in word_nums:
                    if word in temp_str:
                        temp_str = temp_str[-1]

                        if first_value == None:
                            first_value = word_nums.index(word) + 1
                        else:
                            second_value = word_nums.index(word) + 1
                        break

        if second_value == None:
            second_value = first_value

        print(string, first_value, second_value)
        num += int(f"{first_value}{second_value}")

    return num


res_list = format_text(text=text_input)
res = grab_num(text=res_list)
print(res)
