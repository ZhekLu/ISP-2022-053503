from serializer import TOML_STR
from test.testers import SerializerTester


class TomlSerializerTester(SerializerTester):
    TEST_FILE = 'tester_file.toml'
    SERIALIZER_STR = TOML_STR
