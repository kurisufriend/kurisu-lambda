from random import randint


def test(fakepercent, checkpercent, total=100000):
    a = []
    for i in range(100):
        a.append(True)

    for i in range(fakepercent):
        a[i] = False

    timeswon = 0
    for i in range(total):
        won = False
        for i in range(checkpercent):
            b = randint(0, 99)
            if not a[b]: won = True
        if won: timeswon += 1
    return timeswon/total