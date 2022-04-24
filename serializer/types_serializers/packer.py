from accessify import protected, private
import builtins
import inspect
from types import FunctionType, CodeType, LambdaType


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
        return getattr(obj, "__iter__")

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

    @staticmethod
    def pack_function(func):
        pass

    @staticmethod
    def pack_nested(func):
        pass

    @staticmethod
    def pack_class(cl):
        pass

    @staticmethod
    def pack_iterable(it):
        pass

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
