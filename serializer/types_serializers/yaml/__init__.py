from types_serializers import ISerializer
from yaml import load, dump, SafeLoader
import packer


class Yaml:

    # Dump methods

    @staticmethod
    def dumps(obj) -> str:
        return Yaml._str(packer.pack(obj))

    @staticmethod
    def dump(obj, file):
        with open(file, 'w') as f:
            f.write(Yaml.dumps(obj))

    # Load methods

    @staticmethod
    def loads(s: str):
        return packer.unpack(Yaml._object(s))

    @staticmethod
    def load(file: str):
        with open(file, 'r') as f:
            return Yaml.loads(f.read())

    # Additional methods

    # To string methods

    @staticmethod
    def _str(obj) -> str:
        return dump(obj)

    # From string

    @staticmethod
    def _object(obj: _str) -> object:
        return load(obj, SafeLoader)
