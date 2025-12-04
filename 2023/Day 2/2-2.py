from input import text

colors = ["r", "g", "b"]
c_limit = [0, 0, 0]
answer = 0
games = text.split("\n")
for game in games:
    print(game)
    # Game 1: 4 blue, 7 red, 5 green; 3 blue, 4 red, 16 green; 3 red, 11 green
    sets = game.split(":")[1:][0]
    rolls = sets.split(";")
    c_limit = [0, 0, 0]
    for dice in rolls:
        # ["4 blue, 7 red, 5 green", "3 blue, 4 red, 16 green"...]
        res = dice.split(",")
        # print(res)
        for entry in res:
            # "4 blue, 7 red, 5 green"
            # print(entry)
            roll = entry.strip().split(" ")
            val = int(roll[0])
            color = roll[1][0]
            if color in colors:
                # print(val, color, colors.index(color))
                if val > c_limit[colors.index(color)]:
                    c_limit[colors.index(color)] = val

    answer += c_limit[0] * c_limit[1] * c_limit[2]


print(answer)
