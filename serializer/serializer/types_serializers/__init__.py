from typing import Any


class ISerializer:

    @staticmethod
    def dump(obj: Any, file: str) -> None:
        ...
    # TODO!: dump for all

    @staticmethod
    def dumps(obj: Any) -> str:
        ...

    @staticmethod
    def load(file: str) -> Any:
        ...

    @staticmethod
    def loads(s: str) -> Any:
        ...
