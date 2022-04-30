from serializer import JSON_STR
from test.testers import SerializerTester
import unittest


class JsonSerializerTester(SerializerTester):
    TEST_FILE = 'tester_file.json'
    SERIALIZER_STR = JSON_STR


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(JsonSerializerTester())
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()
    # TODO! why all tests ran? @@unittest.skipIf() - skip all
