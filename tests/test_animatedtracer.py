# import sys, os
# sys.path.append('d:/work/python/manim-decorate/src')
# import animatedtracer

# print(os.path)

import inspect

class MyContext:
    def __enter__(self):
        frame = inspect.currentframe().f_back
        source_lines, start_line = inspect.getsourcelines(frame)
        with_block = ''.join(source_lines[start_line-1:])
        print(with_block)
    def __exit__(self, exc_type, exc_value, traceback):
        pass

with MyContext():
    print("Inside context")