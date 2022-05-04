from typing import Any


class ISerializer:

    def dump(self, obj: Any, file: str) -> None:
        with open(file, 'w+') as f:
            f.write(self.dumps(obj))
    # TODO!: dump for all

    def dumps(self, obj: Any) -> str:
        ...

    def load(self, file: str) -> Any:
        with open(file, 'r') as f:
            return self.loads(f.read())

    def loads(self, s: str) -> Any:
        ...
