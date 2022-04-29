from serializer import factory as fc
import unittest
import test.test_source as test_source
import test.test_funcs as test_funcs
import test.test_module as test_module


class SerializeTester(unittest.TestCase):
    # ---------JSON---------
    def test_json_int(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_float(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.float_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_str(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.str_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_boolean(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.boolean_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_none(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.none_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_list(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.list_glob

        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_tuple(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.tuple_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, tuple(new_obj))

    def test_json_set(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.set_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, set(new_obj))

    def test_json_dict(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.dict_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj['Name'], new_obj['Name'])

    def test_json_lambda(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_source.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_json_simple_func(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_funcs.simple_foo
        self.s.dump(old_obj, 'test.json')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(), new_obj())

    def test_json_complex_funcs(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        for i, f in enumerate(test_funcs.funcs[1:]):
            old = f
            new = self.s.loads(self.s.dumps(old))
            if i > 1:
                self.assertEqual(new(2), old(2))
            else:
                self.assertEqual(new(42, 13), old(42, 13))

    def test_json_func_with_module(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_obj = test_module.f
        self.s.dump(old_obj, 'test.json')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(13), new_obj(13))

    def test_json_simple_class(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_class = test_source.SimpleClass
        new_class = self.s.loads(self.s.dumps(old_class))
        old_obj = old_class()
        new_obj = new_class()
        self.assertEqual(old_obj.say_kuku(), new_obj.say_kuku())
        self.assertEqual(old_obj.word, new_obj.word)

    def test_json_complex_class(self):
        self.s = fc.get_serializer(fc.JSON_STR)
        old_class = test_source.ComplexClass
        new_class = self.s.loads(self.s.dumps(old_class))
        old_obj = old_class()
        new_obj = new_class()

        self.assertEqual(old_obj.simple_class.word, new_obj.simple_class.word)
        self.assertEqual(old_obj.func_with_glob(), new_obj.func_with_glob())
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.simple_class.say_kuku(), new_obj.simple_class.say_kuku())


if __name__ == '__main__':
    unittest.main()
