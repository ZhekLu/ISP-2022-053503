import importlib.util
import inspect
import os
import sys
from types import FunctionType, CodeType, LambdaType, ModuleType
from typing import Callable, Iterable, Any


class Packer:

    @staticmethod
    def pack(obj: Any) -> Any:
        if Packer.is_primitive(obj):
            return obj.replace('\\', '/') if isinstance(obj, str) else obj
        if Packer.is_function(obj):
            return Packer.pack_function(obj)
        if inspect.iscode(obj):
            return Packer.pack_nested(obj)
        if inspect.ismodule(obj):
            return Packer.pack_module(obj)
        if inspect.isclass(obj):
            return Packer.pack_class(obj)
        if Packer.is_iterable(obj):
            return Packer.pack_iterable(obj)
        return Packer.pack_object(obj)

    @staticmethod
    def unpack(source: Any) -> Any:
        if Packer.is_primitive(source):
            return source

        if isinstance(source, dict):
            if "__type__" in source.keys():
                source_type = source["__type__"]
                if source_type == "function":
                    return Packer.unpack_function(source)
                if source_type == "code":
                    return Packer.unpack_nested(source)
                if source_type == "module":
                    return Packer.unpack_module(source)
                if source_type == "object":
                    return Packer.unpack_object(source)
                if source_type == "class":
                    return Packer.unpack_class(source)
            return Packer.unpack_iterable(source)

        if Packer.is_iterable(source):
            return Packer.unpack_iterable(source)

    # Additional methods

    # Checkers

    primitives = (int, str, bool, float, type(None),)

    @staticmethod
    def is_primitive(obj: Any) -> bool:
        return isinstance(obj, Packer.primitives)

    @staticmethod
    def is_iterable(obj: Any) -> bool:
        return getattr(obj, "__iter__", None) and not isinstance(obj, str)

    @staticmethod
    def is_function(obj: Any) -> bool:
        return inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, LambdaType)

    @staticmethod
    def is_std_lib_module(module: ModuleType) -> bool:
        python_path = os.path.dirname(sys.executable)
        module_path = importlib.util.find_spec(module.__name__).origin
        return (
                'built-in' in module_path or
                module.__name__ in sys.builtin_module_names or
                python_path not in module_path or
                'site-packages' not in module_path
        )

    # Getters

    @staticmethod
    def get_global_vars(func: FunctionType) -> dict:
        globs = {}
        for global_var in func.__code__.co_names:
            if global_var in func.__globals__:
                globs[global_var] = func.__globals__[global_var]
        return globs

    CODE_ITERS = ('co_code', 'co_consts', 'co_names', 'co_varnames', 'co_lnotab', 'co_freevars', 'co_cellvars')

    @staticmethod
    def get_code(args: dict) -> CodeType:

        for key, value in args.items():
            if key in Packer.CODE_ITERS and not value:
                args[key] = []

        return CodeType(
            args['co_argcount'],
            args['co_posonlyargcount'],
            args['co_kwonlyargcount'],
            args['co_nlocals'],
            args['co_stacksize'],
            args['co_flags'],
            bytes(args['co_code']),
            tuple(args['co_consts']),
            tuple(args['co_names']),
            tuple(args['co_varnames']),
            args['co_filename'],
            args['co_name'],
            args['co_firstlineno'],
            bytes(args['co_lnotab']),
            tuple(args['co_freevars']),
            tuple(args['co_cellvars']))

    # Packers

    FUNC_ATTRS = ["__globals__", "__defaults__", "__kwdefaults__", "__closure__"]

    @staticmethod
    def pack_function(func: FunctionType) -> dict:
        packed = {"__type__": "function", "__name__": func.__name__}
        for attribute in Packer.FUNC_ATTRS:
            check = Packer.get_global_vars(func)
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
            args[arg] = Packer.pack(value)

        packed["__code__"] = args

        return packed

    @staticmethod
    def pack_nested(code: CodeType):
        print("pack:code")
        packed = {"__type__": "code"}

        for key, value in inspect.getmembers(code):
            if key.startswith("co"):
                packed[key] = Packer.pack(value)
        return packed
        # TODO! closure for nested functions??? (it's ok)

    @staticmethod
    def pack_module(module: ModuleType):
        print("pack:module")
        packed = {"__type__": "module", "__name__": module.__name__}
        if Packer.is_std_lib_module(module):
            return packed

        packed["__content__"] = {}
        for key, value in inspect.getmembers(module):
            if not key.startswith("__"):
                packed["__content__"][key] = Packer.pack(value)
        return packed

    @staticmethod
    def pack_class(cl: type) -> dict:
        packed = {'__type__': 'class', '__name__': cl.__name__}
        for attr in dir(cl):
            attr_value = getattr(cl, attr)
            if attr == "__init__":
                packed[attr] = Packer.pack_function(attr_value)
            elif not attr.startswith('__'):
                packed[attr] = Packer.pack(attr_value)
        return packed

    iterables = (list, tuple, set, bytes,)

    @staticmethod
    def pack_iterable(it: Iterable) -> Iterable:
        packed = None
        if isinstance(it, Packer.iterables):
            packed = [Packer.pack(value) for value in it]
        elif isinstance(it, dict):
            packed = {key: Packer.pack(value) for key, value in it.items()}
        return packed

    @staticmethod
    def pack_object(obj: object) -> dict:
        packed = {"__type__": "object", "__class__": obj.__class__.__name__}
        for attr in dir(obj):
            if not attr.startswith("__"):
                value = Packer.pack(getattr(obj, attr))
                packed[attr] = value
        return packed

    # Unpackers

    @staticmethod
    def unpack_function(source: dict) -> FunctionType:
        args = Packer.unpack(source["__code__"])
        global_values = source["__globals__"]

        for name in global_values.keys():
            if name in args["co_names"]:
                global_values[name] = Packer.unpack(global_values[name])

        global_values["__builtins__"] = __import__("builtins")

        consts = []
        for const in args["co_consts"]:
            unpacked = Packer.unpack(const)
            consts.append(unpacked.__code__ if Packer.is_function(unpacked) else const)
        args["co_consts"] = consts

        for arg in Packer.FUNC_ATTRS[1:]:
            if not source[arg]:
                source[arg] = []

        code = Packer.get_code(args)
        f = FunctionType(code=code, globals=global_values,
                         argdefs=tuple(source['__defaults__']), closure=tuple(source['__closure__']))
        f.__kwdefaults__ = dict(source['__kwdefaults__'])

        return f

    @staticmethod
    def unpack_nested(source: dict) -> CodeType:
        print("unpack:code")
        code = {}
        for key, value in source.items():
            unpacked_value = Packer.unpack(value)
            code[key] = unpacked_value

        return Packer.get_code(code)

    @staticmethod
    def unpack_module(source: dict):
        if "__content__" not in source:
            return __import__(source["__name__"])

        module = importlib.util.module_from_spec(source["__name__"])
        for key, value in source["__content__"].items():
            setattr(module, key, Packer.unpack(value))
        return module

    @staticmethod
    def unpack_object(source: dict):
        meta = type(source['__class__'], (), {})
        unpacked = meta()
        for key, value in source.items():
            if key != '__class__':
                setattr(unpacked, key, Packer.unpack(value))
        return unpacked

    @staticmethod
    def unpack_class(source: dict):
        unpacked = Packer.unpack_iterable(source)
        return type(source["__name__"], (), unpacked)

    @staticmethod
    def unpack_iterable(source):
        unpacked = None
        if isinstance(source, Packer.iterables):
            unpacked = [Packer.unpack(i) for i in source]
        elif isinstance(source, dict):
            unpacked = {key: Packer.unpack(value) for key, value in source.items()}
        return unpacked
