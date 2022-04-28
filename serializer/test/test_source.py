int_glob = 73
str_glob = 'global'
float_glob = 2.2
boolean_glob = True
none_glob = None
list_glob = [1, '2', 3.3]
tuple_glob = (1, '2', 3.3)
set_glob = {1, '2', 3.3}
dict_glob = {'Name': 'Good name', 'Age': 42, 'One more key': True}
simple_lambda = lambda q: q * q


class SimpleClass:
    def __init__(self):
        self.can_say = True
        self.count = 5
        self.word = "ku"

    def say_kuku(self):
        return self.word * self.count


class ComplexClass:
    def __init__(self):
        self.simple_class = SimpleClass()
        self.const = int_glob
        self.name = 'ComplexClass'

    def func_with_glob(self):
        return "local_str" + str_glob


class TestClass:
    stat_var = 13

    def __init__(self, a):
        self.var = a

    def __private_method(self):
        self.var += 1

    def method(self):
        return 13 + self.var
