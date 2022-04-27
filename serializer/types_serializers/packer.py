from accessify import protected, private
import builtins
import inspect
from types import FunctionType, CodeType, LambdaType
from typing import Callable, Iterable


class Packer:

    @staticmethod
    def pack(obj: object) -> object:
        if Packer.is_primitive(obj):
            return obj.replace('\\', '/') if isinstance(obj, str) else obj
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
            if "__type__" in source.keys():
                source_type = source["__type__"]
                if source_type == "function":
                    return Packer.unpack_function(source)
                if source_type == "code":
                    return Packer.unpack_nested(source)
                if source_type == "object":
                    return Packer.unpack_object(source)
                if source_type == "class":
                    return Packer.unpack_class(source)
            return Packer.unpack_iterable(source)

        if Packer.is_iterable(source):
            return Packer.unpack_iterable(source)

        return None

    # Additional methods

    # Checkers

    primitives = (int, str, bool, float, type(None), )

    @staticmethod
    def is_primitive(obj: object) -> bool:
        return isinstance(obj, Packer.primitives)

    @staticmethod
    def is_iterable(obj: object) -> bool:
        return getattr(obj, "__iter__", None) and not isinstance(obj, str)

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
            args[arg] = Packer.pack(value)

        packed["__code__"] = args

        return packed

    @staticmethod
    def pack_nested(code: CodeType):
        print("pack:code")
        # f = FunctionType(code, globals={"__builtins__": __import__("builtins")}, closure=())
        # return Packer.pack_function(f)

        packed = {"__type__": "code"}
        for key, value in inspect.getmembers(code):
            if key.startswith("co"):
                packed[key] = Packer.pack(value)
        return packed

        # TODO! closure for nested functions??? (it's ok)
        # return code

    @staticmethod
    def pack_class(cl: object):
        print("class packer is needed")
        pass

    iterables = (list, tuple, set, bytes, )

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
    def unpack_function(source: dict) -> FunctionType:
        args = source["__code__"]
        global_values = source["__globals__"]
        # TODO! builtins?
        for name in global_values.keys():
            if name in args["co_names"]:
                global_values[name] = Packer.unpack(global_values[name])
            # TODO! beautify it.
        global_values["__builtins__"] = __import__("builtins")

        consts = []
        for const in args["co_consts"]:
            unpacked = Packer.unpack(const)
            consts.append(unpacked.__code__ if Packer.is_function(unpacked) else const)
        args["co_consts"] = consts

        for arg in Packer.FUNC_ATTRS[2:]:
            if not source[arg]:
                source[arg] = []

        code = CodeType(
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
        # TODO! too mach code
        f = FunctionType(code=code, globals=global_values,
                         argdefs=tuple(source['__defaults__']), closure=tuple(source['__closure__']))
        f.__kwdefaults__ = dict(source['__kwdefaults__'])

        return f

    CODE_ITERS = ('co_code', 'co_consts', 'co_names', 'co_varnames', 'co_lnotab', 'co_freevars', 'co_cellvars')

    @staticmethod
    def unpack_nested(source: dict) -> CodeType:
        print("unpack:code")
        code = {}
        for key, value in source.items():
            unpacked_value = Packer.unpack(value)
            code[key] = unpacked_value
            if key in Packer.CODE_ITERS and not unpacked_value:
                code[key] = []

        return CodeType(
            code['co_argcount'],
            code['co_posonlyargcount'],
            code['co_kwonlyargcount'],
            code['co_nlocals'],
            code['co_stacksize'],
            code['co_flags'],
            bytes(code['co_code']),
            tuple(code['co_consts']),
            tuple(code['co_names']),
            tuple(code['co_varnames']),
            code['co_filename'],
            code['co_name'],
            code['co_firstlineno'],
            bytes(code['co_lnotab']),
            tuple(code['co_freevars']),
            tuple(code['co_cellvars']))
        # TODO! remove this duplicate
        # return CodeType(**code)

    @staticmethod
    def unpack_object(source: dict):
        pass

    @staticmethod
    def unpack_class(source: dict):
        pass

    @staticmethod
    def unpack_iterable(source):
        unpacked = None
        if isinstance(source, Packer.iterables):
            unpacked = [Packer.unpack(i) for i in source]
        elif isinstance(source, dict):
            unpacked = {key: Packer.unpack(value) for key, value in source.items()}
        return unpacked
