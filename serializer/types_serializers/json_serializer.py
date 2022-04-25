from types_serializers.packer import Packer


class Json:

    # Dump methods

    @staticmethod
    def dumps(obj) -> str:
        return Json.str(Packer.pack(obj))

    @staticmethod
    def dump(obj, file):
        with open(file, 'w') as f:
            f.write(Json.dumps(obj))

    # Load methods
    # TODO!

    # Additional methods

    @staticmethod
    def str(obj, name='') -> str:
        if Packer.is_primitive(obj):
            return Json.str_primitive(obj, name)
        if Packer.is_iterable(obj):
            return Json.str_dict(obj, name) \
                if isinstance(obj, dict) \
                else Json.str_collection(obj, name)
        return Json.str_class(obj, name)

    @staticmethod
    def str_primitive(obj, name) -> str:
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
    def str_collection(obj, name) -> str:
        string = ''
        if name:
            string = f'{name}: '
        string += '['
        # string += f'["__{type(obj).__name__}__", '
        for i in range(len(obj)):
            string += Json.str(obj[i])
            if i < len(obj) - 1:
                string += ', '
        return string + ']'

    @staticmethod
    def str_dict(obj: dict, name) -> str:
        string = ''
        if name:
            string = f'{name}: '
        string += '{'
        len(obj)
        for i, (key, value) in enumerate(obj.items()):
            string += Json.str(value, Json.str(str(key)))
            if i < len(obj) - 1:
                string += ', '
        return string + '}'

    @staticmethod
    def str_class(obj, name) -> str:
        return "class object"
