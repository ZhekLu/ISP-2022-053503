from types_serializers import ISerializer
from types_serializers.json import Json
from types_serializers.toml import Toml
from types_serializers.yaml import Yaml


def get_serializer(format_type: str) -> ISerializer:
    if format_type == 'json':
        return Json
    if format_type == 'toml':
        return Toml
    if format_type == 'yaml':
        return Yaml
    raise TypeError(f'Unknown format type {format_type}')
