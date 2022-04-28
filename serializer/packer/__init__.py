from types import FunctionType, CodeType, LambdaType, ModuleType
from typing import Iterable, Any
import importlib.util
import inspect
import os
import sys


def pack(obj: Any) -> Any:
    if is_primitive(obj):
        return obj.replace('\\', '/') if isinstance(obj, str) else obj
    if is_function(obj):
        return _pack_function(obj)
    if inspect.iscode(obj):
        return _pack_nested(obj)
    if inspect.ismodule(obj):
        return _pack_module(obj)
    if inspect.isclass(obj):
        return _pack_class(obj)
    if is_iterable(obj):
        return _pack_iterable(obj)
    return _pack_object(obj)


def unpack(source: Any) -> Any:
    if is_primitive(source):
        return source

    if isinstance(source, dict):
        if "__type__" in source.keys():
            source_type = source["__type__"]
            if source_type == "function":
                return _unpack_function(source)
            if source_type == "code":
                return _unpack_nested(source)
            if source_type == "module":
                return _unpack_module(source)
            if source_type == "object":
                return _unpack_object(source)
            if source_type == "class":
                return _unpack_class(source)
        return _unpack_iterable(source)

    if is_iterable(source):
        return _unpack_iterable(source)

# Additional methods

# Checkers


_primitives = (int, str, bool, float, type(None),)


def is_primitive(obj: Any) -> bool:
    return isinstance(obj, _primitives)


def is_iterable(obj: Any) -> bool:
    return getattr(obj, "__iter__", None) and not isinstance(obj, str)


def is_function(obj: Any) -> bool:
    return inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, LambdaType)


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


def _get_global_vars(func: FunctionType) -> dict:
    globs = {}
    for global_var in func.__code__.co_names:
        if global_var in func.__globals__:
            globs[global_var] = func.__globals__[global_var]
    return globs


_CODE_ITERS = ('co_code', 'co_consts', 'co_names', 'co_varnames', 'co_lnotab', 'co_freevars', 'co_cellvars')


def _get_code(args: dict) -> CodeType:

    for key, value in args.items():
        if key in _CODE_ITERS and not value:
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


_FUNC_ATTRS = ["__globals__", "__defaults__", "__kwdefaults__", "__closure__"]


def _pack_function(func: FunctionType) -> dict:
    packed = {"__type__": "function", "__name__": func.__name__}
    for attribute in _FUNC_ATTRS:
        packed[attribute] = _pack_iterable(
            func.__getattribute__(attribute)
            if attribute != "__globals__"
            else _get_global_vars(func)
        )

    args = {}
    for arg, value in inspect.getmembers(func.__code__):
        if not arg.startswith("co_"):
            continue
        if isinstance(value, bytes):
            value = list(value)
        args[arg] = pack(value)

    packed["__code__"] = args

    return packed


def _pack_nested(code: CodeType):
    print("pack:code")
    packed = {"__type__": "code"}

    for key, value in inspect.getmembers(code):
        if key.startswith("co"):
            packed[key] = pack(value)
    return packed
    # TODO! closure for nested functions??? (it's ok)


def _pack_module(module: ModuleType):
    print("pack:module")
    packed = {"__type__": "module", "__name__": module.__name__}
    if is_std_lib_module(module):
        return packed

    packed["__content__"] = {}
    for key, value in inspect.getmembers(module):
        if not key.startswith("__"):
            packed["__content__"][key] = pack(value)
    return packed


def _pack_class(cl: type) -> dict:
    packed = {'__type__': 'class', '__name__': cl.__name__}
    for attr in dir(cl):
        attr_value = getattr(cl, attr)
        if attr == "__init__":
            packed[attr] = _pack_function(attr_value)
        elif not attr.startswith('__'):
            packed[attr] = pack(attr_value)
    return packed


_ITERABLES = (list, tuple, set, bytes,)


def _pack_iterable(it: Iterable) -> Iterable:
    packed = None
    if isinstance(it, _ITERABLES):
        packed = [pack(value) for value in it]
    elif isinstance(it, dict):
        packed = {key: pack(value) for key, value in it.items()}
    return packed


def _pack_object(obj: object) -> dict:
    packed = {"__type__": "object", "__class__": obj.__class__.__name__}
    for attr in dir(obj):
        if not attr.startswith("__"):
            value = pack(getattr(obj, attr))
            packed[attr] = value
    return packed

# Unpackers


def _unpack_function(source: dict) -> FunctionType:
    args = unpack(source["__code__"])
    global_values = source["__globals__"]

    for name in global_values.keys():
        if name in args["co_names"]:
            global_values[name] = unpack(global_values[name])

    global_values["__builtins__"] = __import__("builtins")

    consts = []
    for const in args["co_consts"]:
        unpacked = unpack(const)
        consts.append(unpacked.__code__ if is_function(unpacked) else const)
    args["co_consts"] = consts

    for arg in _FUNC_ATTRS[1:]:
        if not source[arg]:
            source[arg] = []

    code = _get_code(args)
    f = FunctionType(code=code, globals=global_values,
                     argdefs=tuple(source['__defaults__']), closure=tuple(source['__closure__']))
    f.__kwdefaults__ = dict(source['__kwdefaults__'])

    return f


def _unpack_nested(source: dict) -> CodeType:
    print("unpack:code")
    code = {}
    for key, value in source.items():
        unpacked_value = unpack(value)
        code[key] = unpacked_value

    return _get_code(code)


def _unpack_module(source: dict) -> ModuleType:
    if "__content__" not in source:
        return __import__(source["__name__"])

    module = importlib.util.module_from_spec(source["__name__"])
    for key, value in source["__content__"].items():
        setattr(module, key, unpack(value))
    return module


def _unpack_object(source: dict) -> Any:
    meta = type(source['__class__'], (), {})
    unpacked = meta()
    for key, value in source.items():
        if key != '__class__':
            setattr(unpacked, key, unpack(value))
    return unpacked


def _unpack_class(source: dict) -> type:
    unpacked = _unpack_iterable(source)
    return type(source["__name__"], (), unpacked)


def _unpack_iterable(source) -> Any:
    unpacked = None
    if isinstance(source, _ITERABLES):
        unpacked = [unpack(i) for i in source]
    elif isinstance(source, dict):
        unpacked = {key: unpack(value) for key, value in source.items()}
    return unpacked
