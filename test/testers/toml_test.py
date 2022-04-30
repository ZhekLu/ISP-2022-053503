from test.testers import SerializerTester, factory
import unittest


class TomlSerializerTester(SerializerTester):
    TEST_FILE = 'tester_file.toml'
    SERIALIZER_STR = factory.TOML_STR


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TomlSerializerTester())
    unittest.TextTestRunner(verbosity=2).run(suite)
