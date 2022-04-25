from types_serializers.packer import Packer


class Toml:

    # Dump methods

    @staticmethod
    def dumps(obj) -> str:
        return Toml.str(Packer.pack(obj))

    @staticmethod
    def dump(obj, file):
        with open(file, 'w') as f:
            f.write(Toml.dumps(obj))

    # Load methods

    @staticmethod
    def loads(s: str):
        return Packer.unpack(Toml.object(s))

    @staticmethod
    def load(file: str):
        with open(file, 'r') as f:
            return Toml.loads(f.read())

    # Additional methods

    # To string methods

    @staticmethod
    def str(obj, name='', name_path='') -> str:
        if Packer.is_primitive(obj):
            return Toml.str_primitive(obj, name)
        if isinstance(obj, dict):
            return Toml.str_dict(obj, name, name_path)
        if Packer.is_iterable(obj):
            return Toml.str_collection(obj, name)

    @staticmethod
    def str_primitive(obj, name) -> str:
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
    def str_collection(obj, name) -> str:
        string = ''
        if name:
            string = f'{name} = '
        string += '['
        for i in range(len(obj)):
            string += Toml.str(obj[i])
            if i < len(obj) - 1:
                string += ', '
        return string + ']'

    @staticmethod
    def str_dict(obj: dict, name: str, name_path: str) -> str:
        string = ''
        if name:
            string = f'[{name}]\n'

        for key, value in obj.items():
            string += Toml.str(value, Toml.str(str(key)), name)
            string += '\n'
        return string

    # From string

    @staticmethod
    def object(obj: str) -> object:
        return None
