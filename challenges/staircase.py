def staircase(n):
    for i in range(1, n + 1):
        print("_" * (n - i) + "#" * i)


staircase(6)
