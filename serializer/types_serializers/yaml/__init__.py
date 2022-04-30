from serializer.types_serializers import ISerializer
import serializer.packer as packer
from typing import Any
import yaml


class Yaml(ISerializer):

    # Dump methods

    @staticmethod
    def dumps(obj: Any) -> str:
        return Yaml._str(packer.pack(obj))

    @staticmethod
    def dump(obj: Any, file: str) -> None:
        with open(file, 'w') as f:
            f.write(Yaml.dumps(obj))

    # Load methods

    @staticmethod
    def loads(s: str) -> Any:
        return packer.unpack(Yaml._object(s))

    @staticmethod
    def load(file: str) -> Any:
        with open(file, 'r') as f:
            return Yaml.loads(f.read())

    # Additional methods

    # To string methods

    @staticmethod
    def _str(obj: Any) -> str:
        return yaml.dump(obj)

    # From string

    @staticmethod
    def _object(obj: str) -> object:
        return yaml.load(obj, yaml.SafeLoader)
