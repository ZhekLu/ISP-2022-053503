from serializer import JSON_STR
from test.testers import SerializerTester


class JsonSerializerTester(SerializerTester):
    TEST_FILE = 'tester_file.json'
    SERIALIZER_STR = JSON_STR
