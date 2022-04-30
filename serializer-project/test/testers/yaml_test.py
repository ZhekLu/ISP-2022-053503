from serializer import YAML_STR
from test.testers import SerializerTester


class YamlSerializerTester(SerializerTester):
    TEST_FILE = 'tester_file.yaml'
    SERIALIZER_STR = YAML_STR
