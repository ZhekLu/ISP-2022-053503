from serializer.types_serializers import ISerializer
from serializer.types_serializers.json import Json
from serializer.types_serializers.toml import Toml
from serializer.types_serializers.yaml import Yaml

JSON_STR = 'json'
YAML_STR = 'yaml'
TOML_STR = 'toml'


def get_serializer(format_type: str) -> ISerializer:
    if format_type == 'json':
        return Json
    if format_type == 'toml':
        return Toml
    if format_type == 'yaml':
        return Yaml
    raise TypeError(f'Unknown format type {format_type}')
    # TODO! why there's type warn?
