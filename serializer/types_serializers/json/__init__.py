from types_serializers import ISerializer
import packer


class Json(ISerializer):

    # Dump methods

    @staticmethod
    def dumps(obj) -> str:
        return Json._str(packer.pack(obj))

    @staticmethod
    def dump(obj, file):
        with open(file, 'w') as f:
            f.write(Json.dumps(obj))

    # Load methods

    @staticmethod
    def loads(s: str):
        return packer.unpack(Json._object(s))

    @staticmethod
    def load(file: str):
        with open(file, 'r') as f:
            return Json.loads(f.read())

    # Additional methods

    # To string methods

    @staticmethod
    def _str(obj, name='') -> str:
        if packer.is_primitive(obj):
            return Json._str_primitive(obj, name)
        if packer.is_iterable(obj):
            return Json._str_dict(obj, name) \
                if isinstance(obj, dict) \
                else Json._str_collection(obj, name)
        return Json._str_class(obj, name)

    @staticmethod
    def _str_primitive(obj, name) -> _str:
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
    def _str_collection(obj, name) -> _str:
        string = ''
        if name:
            string = f'{name}: '
        string += '['
        # string += f'["__{type(obj).__name__}__", '
        for i in range(len(obj)):
            string += Json._str(obj[i])
            if i < len(obj) - 1:
                string += ', '
        return string + ']'

    @staticmethod
    def _str_dict(obj: dict, name) -> _str:
        string = ''
        if name:
            string = f'{name}: '
        string += '{'

        for i, (key, value) in enumerate(obj.items()):
            string += Json._str(value, Json._str(str(key)))
            if i < len(obj) - 1:
                string += ', '
        return string + '}'

    @staticmethod
    def _str_class(obj, name) -> _str:
        return "class object"

    # From string

    @staticmethod
    def _object(obj: _str) -> object:
        return eval(obj.replace('null', "None")) \
            if obj \
            else None
