from input import text

colors = ["r", "g", "b"]
c_limit = [12, 13, 14]
answer = 0
games = text.split("\n")
for game in games:
    print(game)
    # Game 1: 4 blue, 7 red, 5 green; 3 blue, 4 red, 16 green; 3 red, 11 green
    sets = game.split(":")[1:][0]
    rolls = sets.split(";")
    gg = True
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
                    gg = False
                    break

        if gg == False:
            print(f"Game {game.split(":")[0][4:].strip()} is impossible.")
            break

    if gg:
        answer += int(game.split(":")[0][4:].strip())


print(answer)
