from serializer.types_serializers import ISerializer
import serializer.packer as packer


class Toml(ISerializer):

    # Dump methods

    @staticmethod
    def dumps(obj) -> str:
        return Toml._str(packer.pack(obj))

    @staticmethod
    def dump(obj, file):
        with open(file, 'w') as f:
            f.write(Toml.dumps(obj))

    # Load methods

    @staticmethod
    def loads(s: str):
        return packer.unpack(Toml._object(s))

    @staticmethod
    def load(file: str):
        with open(file, 'r') as f:
            return Toml.loads(f.read())

    # Additional methods

    # To string methods

    @staticmethod
    def _str(obj, name='', name_path='') -> str:
        # s = toml.dumps(obj)
        # d = toml.loads(s.replace('\\', '/'))
        # return toml.dumps(obj)
        if packer.is_primitive(obj):
            return Toml._str_primitive(obj, name)
        if isinstance(obj, dict):
            return Toml._str_dict(obj, name, name_path)
        if packer.is_iterable(obj):
            return Toml._str_collection(obj, name)

    @staticmethod
    def _str_primitive(obj, name) -> str:
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
    def _str_collection(obj, name: str) -> str:
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
        if name:
            pre_name = f'{name_path}.' if name_path else ''
            string = f'[{pre_name + name}]\n'

        for key, value in obj.items():
            string += Toml._str(value, Toml._str(str(key)), name)
            string += '\n'
        return string + '\n'

    # From string

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
    def _object_collection(obj: str) -> object:
        return Toml._object_primitive(obj)

    @staticmethod
    def _object_dict(obj: str) -> object:
        parsed = {}

        # check for other
        other_start = obj.find('[')
        if other_start != 0 and other_start != 1:
            other_start = obj.find('\n[')
            if other_start != -1:
                other_start += 1
        while obj and other_start != -1:
            other_end = obj.find(']')
            var_name = obj[other_start + 1:other_end]
            other_start_in, other_end = other_end + 2, obj.find('\n\n')
            parsed[var_name] = Toml._object_dict(obj[other_start_in:other_end])
            if not parsed[var_name]:
                other_end += 1
            obj = obj[:other_start] + obj[other_end + 2:]
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
