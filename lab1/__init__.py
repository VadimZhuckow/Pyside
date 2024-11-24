a = [1, -1, -2, 2, -4, 3]


def t1(x):
    return x < -1


m1 = filter(t1, a)

print(list(m1))
