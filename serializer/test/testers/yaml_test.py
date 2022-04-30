from serializer import YAML_STR
from test.testers import SerializerTester
import unittest


class YamlSerializerTester(SerializerTester):
    TEST_FILE = 'tester_file.yaml'
    SERIALIZER_STR = YAML_STR


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(YamlSerializerTester())
    unittest.TextTestRunner(verbosity=2).run(suite)
