from serializer.types_serializers import ISerializer
import serializer.packer as packer
from typing import Any, Sequence


class Json(ISerializer):

    # Dump methods

    def dumps(self, obj: Any) -> str:
        return self._str(packer.pack(obj))

    # Load methods

    def loads(self, s: str) -> Any:
        return packer.unpack(Json._object())

    # Additional methods

    # To string methods

    @staticmethod
    def _str(obj: Any, name: str = '') -> str:
        if packer.is_primitive(obj):
            return Json._str_primitive(name)
        if packer.is_iterable(obj):
            return Json._str_dict(name) \
                if isinstance(obj, dict) \
                else Json._str_collection(name)

    @staticmethod
    def _str_primitive(obj: object, name: str) -> str:
        string = ''
        if name:
            string = f'{name}: '
        if obj is None:
            string += 'null'
        elif isinstance(obj, bool):
            string += 'true' if obj else 'false'
        elif isinstance(obj, (int, float)):
            string += str(obj)
        elif isinstance(obj, str):
            string += f'"{obj}"'
        return string

    @staticmethod
    def _str_collection(obj: Sequence, name: str) -> str:
        string = ''
        if name:
            string = f'{name}: '
        string += '['
        # string += f'["__{type(obj).__name__}__", '
        for i in range(len(obj)):
            string += Json._str()
            if i < len(obj) - 1:
                string += ', '
        return string + ']'

    @staticmethod
    def _str_dict(obj: dict, name: str) -> str:
        string = ''
        if name:
            string = f'{name}: '
        string += '{'

        for i, (key, value) in enumerate(obj.items()):
            string += Json._str(Json._str())
            if i < len(obj) - 1:
                string += ', '
        return string + '}'

    # From string

    @staticmethod
    def _process(obj: str) -> str:
        return obj.replace('null', 'None').replace('true', 'True').replace('false', 'False')

    @staticmethod
    def _object(obj: str) -> object:
        return eval(Json._process()) \
            if obj \
            else None
