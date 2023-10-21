from SortAnimate import Sort
import functools
import inspect
import sys
import pysnooper

class Tracer():

    def __enter__(self):
        print('__enter__()')
        sys.settrace(self.trace)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.settrace(None)
        print('__exit__()')
        # sys.settrace(self.trace)

    def __init__(self) -> None:
        print('__init__()')

    def __call__(self, function_or_class):
        print('__call__()')
        return self._wrap_function(function_or_class)

    def _wrap_function(self, function):
        print('_wrap_function')
        @functools.wraps(function)
        def simple_wrapper(*args, **kwargs):
            with self:
                return function(*args, **kwargs)

        return simple_wrapper

    def _is_internal_frame(self, frame):
        return frame.f_code.co_filename == Tracer.__enter__.__code__.co_filename

    def trace(self, frame, event, arg):
        if not self._is_internal_frame(frame):
            return None
        else:

            print(f'trace: frame={frame}, event={event}, arg={arg}')
            return self.trace

# @pysnooper.snoop()
# @Tracer()
# def bubble_sort(arr):
#     for i in range(1, len(arr)):
#         for j in range(0, len(arr)-i):
#             if arr[j] > arr[j+1]:
#                 arr[j], arr[j+1] = arr[j+1], arr[j]
#     return arr

# bubble_sort([1,2,3])

@Tracer()
def simple():
    return 1

simple()