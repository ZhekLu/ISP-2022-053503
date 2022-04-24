glob = 1


def simple_foo():
    return 1


def foo_with_args(a, b):
    return a + b


def foo_with_def_args(a, d, b=3, *args, c=None):
    return a + b


def foo_with_glob(a):
    return glob + a


def foo_with_glob_foo(a):
    return foo_with_glob(a)


# TODO; for this type
def foo_with_nested_foo(arg):
    def foo(b):
        return b + arg
    # print(foo.__closure__)
    return foo
# print(foo_with_nested_foo.__code__.co_lnotab)

def foo_with_vars(index):
    l = [1, 2, 3, 4]
    return l[index]


funcs = [simple_foo, foo_with_args, foo_with_def_args,
         foo_with_glob, foo_with_glob_foo, foo_with_nested_foo, foo_with_vars]


