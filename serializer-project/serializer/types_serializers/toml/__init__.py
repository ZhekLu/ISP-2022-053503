from serializer.types_serializers import ISerializer
import serializer.packer as packer
from typing import Any, Sequence


class Toml(ISerializer):

    # Dump methods

    @staticmethod
    def dumps(obj: Any) -> str:
        return Toml._str(packer.pack(obj))

    @staticmethod
    def dump(obj: Any, file: str) -> None:
        with open(file, 'w+') as f:
            f.write(Toml.dumps(obj))

    # Load methods

    @staticmethod
    def loads(s: str) -> Any:
        return packer.unpack(Toml._object(s))

    @staticmethod
    def load(file: str) -> Any:
        with open(file, 'r') as f:
            return Toml.loads(f.read())

    # Additional methods

    # To string methods

    @staticmethod
    def _str(obj: Any, name: str = '', name_path: str = '') -> str:
        if packer.is_primitive(obj):
            return Toml._str_primitive(obj, name)
        if isinstance(obj, dict):
            return Toml._str_dict(obj, name, name_path)
        if packer.is_iterable(obj):
            return Toml._str_collection(obj, name)

    @staticmethod
    def _str_primitive(obj: object, name) -> str:
        string = ''
        if name:
            string = f'{name} = '
        if obj is None:
            string += 'null'
        elif isinstance(obj, bool):
            string += 'true' if obj else 'false'
        elif isinstance(obj, (int, float)):
            string += str(obj)
        elif isinstance(obj, str):
            string += f'"{obj}"' if name else obj
        return string

    @staticmethod
    def _str_collection(obj: Sequence, name: str) -> str:
        string = ''
        if name:
            string = f'{name} = '
        string += '['
        for i in range(len(obj)):
            obj_str = Toml._str(obj[i])
            string += str(f'"{obj_str}"') if isinstance(obj[i], str) else obj_str
            if i < len(obj) - 1:
                string += ', '
        return string + ']'

    @staticmethod
    def _str_dict(obj: dict, name: str, name_path: str) -> str:
        string = ''
        full_name = f'{name_path}.{name}' if name_path else name
        if name:
            string = f'[{full_name}]\n'

        for key, value in obj.items():
            string += Toml._str(value, Toml._str(str(key)), full_name)
            string += '\n'
        if not name_path:
            string += '\n'
        return string + '\r'

    # From string

    @staticmethod
    def _object_name(name: str) -> str:
        index = name.rfind('.')
        if index != -1:
            name = name[index + 1:]
        return name

    @staticmethod
    def _object(obj: str) -> object:
        if not obj:
            return obj
        if '=' in obj:
            return Toml._object_dict(obj)
        if '[' in obj:
            return Toml._object_collection(obj)
        return Toml._object_primitive(obj)

    @staticmethod
    def _object_primitive(obj: str) -> object:
        obj = obj.replace('null', 'None').replace('true', 'True').replace('false', "False")
        try:
            return eval(obj)
        except SyntaxError:
            return eval(str(f'"{obj}"'))

    @staticmethod
    def _object_collection(obj: str) -> Sequence:
        return Toml._object_primitive(obj)

    @staticmethod
    def _object_dict(obj: str) -> dict:
        parsed = {}

        # check for other
        other_start = obj.find('[')
        if other_start != 0 and other_start != 1:
            other_start = obj.find('\n[')
            if other_start != -1:
                other_start += 1
        while obj and other_start != -1:
            other_end = other_start + obj[other_start:].find(']')
            full_name = obj[other_start + 1:other_end]
            var_name = Toml._object_name(full_name)
            other_start_in = other_end + 2

            flag = True
            counter = 0
            while flag:
                other_end = other_end + 2 + obj[other_end + 2:].find('\r')
                counter += 1
                if other_end == -1:
                    other_end = len(obj)
                    flag = False
                elif obj[:other_end].count(f'[{full_name}.') < counter:
                    flag = False

            parsed[var_name] = Toml._object_dict(obj[other_start_in:other_end])
            other_end = other_end + 3 \
                if other_end + 2 < len(obj) and obj[other_end + 2] == '\n' \
                else other_end + 2
            obj = obj[:other_start] + obj[other_end:]
            other_start = obj.find('\n[')
            if other_start != -1:
                other_start += 1

        while obj:
            index = obj.find('=')
            if index == -1:
                return parsed
            var_name = obj[:index - 1]
            obj = obj[index + 2:]
            end_value = obj.find('\n')
            if end_value == -1:
                end_value = len(obj)
            parsed[var_name] = Toml._object(obj[:end_value])
            obj = obj[end_value + 1:]
        return parsed
