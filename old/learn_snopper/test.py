import inspect
import pysnooper
def trace(func):
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe()
        print(f'Function name: {frame.f_code.co_name}')
        print(f'File name: {frame.f_code.co_filename}')
        print(f'Line number: {frame.f_lineno}')
        return func(frame, *args, **kwargs)
    return wrapper

@pysnooper.snoop()
def foo(frame):
    print('Hello, world!')

foo()