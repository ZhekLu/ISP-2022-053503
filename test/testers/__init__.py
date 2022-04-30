from serializer import factory
import test.src.test_source as test_source
import test.src.test_funcs as test_funcs
import test.src.test_module as test_module
import unittest


class SerializerTester(unittest.TestCase):
    TEST_FILE = None
    SERIALIZER_STR = None

    def test_int(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_float(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.float_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_str(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.str_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_boolean(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.boolean_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_none(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.none_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_list(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.list_glob

        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_tuple(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.tuple_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, tuple(new_obj))

    def test_set(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.set_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, set(new_obj))

    def test_dict(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.dict_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj['Name'], new_obj['Name'])

    def test_lambda(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_source.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_simple_func(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_funcs.simple_foo
        self.s.dump(old_obj, self.TEST_FILE)
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(), new_obj())

    def test_foo_with_args(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_funcs.foo_with_args
        self.s.dump(old_obj, self.TEST_FILE)
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(13, 42), new_obj(13, 42))

    def test_foo_with_def_args(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_funcs.foo_with_def_args
        self.s.dump(old_obj, self.TEST_FILE)
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(13, 42), new_obj(13, 42))
        self.assertEqual(old_obj(13, 42, 33), new_obj(13, 42, 33))

    def test_foo_with_glob(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_funcs.foo_with_glob
        self.s.dump(old_obj, self.TEST_FILE)
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(13), new_obj(13))

    def test_foo_with_glob_foo(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_funcs.foo_with_glob_foo
        self.s.dump(old_obj, self.TEST_FILE)
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(13), new_obj(13))

    def test_foo_with_vars(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_funcs.foo_with_vars
        self.s.dump(old_obj, self.TEST_FILE)
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(3), new_obj(3))

    def test_func_with_module(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_obj = test_module.f
        self.s.dump(old_obj, self.TEST_FILE)
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(13), new_obj(13))

    def test_simple_class(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_class = test_source.SimpleClass
        new_class = self.s.loads(self.s.dumps(old_class))
        old_obj = old_class()
        new_obj = new_class()
        self.assertEqual(old_obj.say_kuku(), new_obj.say_kuku())
        self.assertEqual(old_obj.word, new_obj.word)

    def test_complex_class(self):
        self.s = factory.get_serializer(self.SERIALIZER_STR)
        old_class = test_source.ComplexClass
        new_class = self.s.loads(self.s.dumps(old_class))
        old_obj = old_class()
        new_obj = new_class()

        self.assertEqual(old_obj.simple_class.word, new_obj.simple_class.word)
        self.assertEqual(old_obj.func_with_glob(), new_obj.func_with_glob())
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.simple_class.say_kuku(), new_obj.simple_class.say_kuku())
