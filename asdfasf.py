import functools


def decorator(start: str):

    def top_wrapper(func):

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return (start + result).upper()

        return wrapper

    return top_wrapper


@decorator('fooo:')
def convertor(value):
    """My function"""
    return str(value)


FUNCTION_LIST = []


def register(func):
    global FUNCTION_LIST
    FUNCTION_LIST.append(func)
    return func


# convertor = decorator(convertor)


# print(convertor.__name__)
# print(convertor.__doc__)

print(convertor("dasdas"))
# print(new_func("dasdas"))

# help(convertor)


@register
def add(a, b):
    return a + b

@register
def mul(a, b):
    return a * b


print(FUNCTION_LIST)
