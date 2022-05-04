from serializer.types_serializers import ISerializer
import serializer.packer as packer
from typing import Any
import yaml


class Yaml(ISerializer):

    # Dump methods

    def dumps(self, obj: Any) -> str:
        return Yaml._str(packer.pack(obj))

    # Load methods

    def loads(self, s: str) -> Any:
        return packer.unpack(Yaml._object(s))

    # Additional methods

    # To string methods

    @staticmethod
    def _str(obj: Any) -> str:
        return yaml.dump(obj)

    # From string

    @staticmethod
    def _object(obj: str) -> object:
        return yaml.load(obj, yaml.SafeLoader)
