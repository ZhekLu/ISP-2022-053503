from yaml import load, dump, SafeLoader
import packer


class Yaml:

    # Dump methods

    @staticmethod
    def dumps(obj) -> str:
        return Yaml.str(packer.pack(obj))

    @staticmethod
    def dump(obj, file):
        with open(file, 'w') as f:
            f.write(Yaml.dumps(obj))

    # Load methods

    @staticmethod
    def loads(s: str):
        return packer.unpack(Yaml.object(s))

    @staticmethod
    def load(file: str):
        with open(file, 'r') as f:
            return Yaml.loads(f.read())

    # Additional methods

    # To string methods

    @staticmethod
    def str(obj) -> str:
        return dump(obj)

    # From string

    @staticmethod
    def object(obj: str) -> object:
        return load(obj, SafeLoader)
