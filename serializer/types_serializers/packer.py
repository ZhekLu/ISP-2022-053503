from accessify import protected, private
import builtins
import inspect
from types import FunctionType, CodeType, LambdaType
from typing import Callable, Iterable


class Packer:

    @staticmethod
    def pack(obj: object):
        if Packer.is_primitive(obj) or obj is None:
            return obj
        if Packer.is_function(obj):
            return Packer.pack_function(obj)
        if inspect.iscode(obj):
            return Packer.pack_nested(obj)
        if inspect.isclass(obj):
            return Packer.pack_class(obj)
        if Packer.is_iterable(obj):
            return Packer.pack_iterable(obj)
        return Packer.pack_object(obj)

    @staticmethod
    def unpack(source):
        if Packer.is_primitive(source):
            return source

        if isinstance(source, dict):
            if "function" in source.values():
                return Packer.unpack_function(source)
            if "object" in source.values():
                return Packer.unpack_object(source)
            if "class" in source.values():
                return Packer.unpack_class(source)
            return Packer.unpack_iterable(source)

        if Packer.is_iterable(source):
            return Packer.unpack_iterable(source)

        return None

    # Additional methods

    # Checkers

    primitives = (int, str, bool, float,)

    @staticmethod
    def is_primitive(obj: object) -> bool:
        return isinstance(obj, Packer.primitives)

    @staticmethod
    def is_iterable(obj: object) -> bool:
        return getattr(obj, "__iter__", None)

    @staticmethod
    def is_function(obj: object) -> bool:
        return inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, LambdaType)

    @staticmethod
    def get_global_vars(func) -> dict:
        globs = {}
        for global_var in func.__code__.co_names:
            if global_var in func.__globals__:
                globs[global_var] = func.__globals__[global_var]
        return globs

    # Packers

    FUNC_ATTRS = ["__name__", "__globals__", "__defaults__", "__kwdefaults__", "__closure__"]

    @staticmethod
    def pack_function(func: Callable) -> dict:
        if inspect.ismethod(func):
            print("func:method")
            func = func.__func__  # TODO?

        packed = {"__type__": "function"}
        for attribute in Packer.FUNC_ATTRS:
            packed[attribute] = Packer.pack_iterable(
                func.__getattribute__(attribute)
                if attribute != "__globals__"
                else Packer.get_global_vars(func)
            )

        args = {}
        for arg, value in inspect.getmembers(func.__code__):
            if not arg.startswith("co_"):
                continue
            if isinstance(value, bytes):
                value = list(value)
            if Packer.is_iterable(value) and not isinstance(value, str):
                value = [Packer.pack(v) for v in value]
            args[arg] = value

        packed["__code__"] = args

        return packed

    @staticmethod
    def pack_nested(func):
        pass

    @staticmethod
    def pack_class(cl):
        pass

    iterables = (list, tuple, set,)

    @staticmethod
    def pack_iterable(it: Iterable) -> Iterable:
        packed = None
        if isinstance(it, Packer.iterables):
            packed = [Packer.pack(value) for value in it]
        elif isinstance(it, dict):
            packed = {key: Packer.pack(value) for key, value in it.items()}
        return packed

    @staticmethod
    def pack_object(obj):
        pass

    # Unpackers

    @staticmethod
    def unpack_function(source):
        pass

    @staticmethod
    def unpack_object(source):
        pass

    @staticmethod
    def unpack_class(source):
        pass

    @staticmethod
    def unpack_iterable(source):
        pass
