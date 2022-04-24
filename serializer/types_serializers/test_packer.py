from packer import Packer

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


def foo_with_nested_foo(a):
    def foo(b):
        return b + a
    return foo(13)


funcs = [simple_foo, foo_with_args, foo_with_def_args, foo_with_glob, foo_with_glob_foo, foo_with_nested_foo]


for f in funcs:
    for key, value in Packer.pack(f).items():
        print(key, end=':')
        if not isinstance(value, str) and value:
            for i in value.items():
                print(i)
        else:
            print(value)
