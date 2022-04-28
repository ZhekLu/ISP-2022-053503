import math

# first level

c = 42


def f(x):
    a = 123
    return math.sin(x * a * c)


# print(f.__code__.co_names)
# print(f.__globals__)
# second level

d = 5


def t(arg):
    c = 2

    def _f(arg):
        a = 123
        return math.sin(arg * a * c * d)

    return _f(arg)


# print(t.__code__.co_names)
# print(t.__globals__)
