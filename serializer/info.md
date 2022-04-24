## Attributes
- **co_names** is a tuple of global variable names
- **co_varnames** is a tuple of local variable names (and argument names).
- **co_consts** contains (None, ..) as it default return value for a function. 
- **co_posonlyargcount** number of positional only arguments
- **co_kwonlyargcount** number of keyword only arguments (not including ** arg)
- **co_varnames** tuple of names of arguments and local variables
_________________________________________________________
- **__ globals__**: A reference to the dictionary that holds the function’s global variables — the global namespace of the module in which the function was defined.
- **__ defaults__** attribute holds a tuple containing the default argument values for the positional arguments that have defaults, or None if no arguments have a default value.
- **__ kwdefaults__** attribute holds a dict containing defaults for keyword-only arguments.
- **__ closure__** connected to [co_freevars, co_cellvars]
- 