import sys
from pysnooper import snoop as snooptracer  # 以后改成自己的tracer
from manim import Scene
from rich import print, inspect

class AnimatedTracer(snooptracer, Scene):
    def __init__(self, *args, **kwargs):
        snooptracer.__init__(self, *args, **kwargs)
        Scene.__init__(self)
        # self.color = self.color or sys.platform in ('win32',)

        self.write = lambda s: None

    def on_elapsed_time(self, start_time, elapsed_time_string):
        print('on_elapsed_time', start_time, elapsed_time_string)

    def on_source_path(self, source_path):
        print('on_source_path', source_path)

    def on_newish_variable(self, newish_string, name, value_repr):
        print('on_newish_variable', newish_string, name, value_repr)

    def on_modified_variable(self, name, value_repr):
        print('on_modified_variable', name, value_repr)

    def on_finished_line(self, timestamp, thread_info, event, line_no, source_line):
        print('on_finished_line', timestamp, thread_info, event, line_no, source_line)

    def on_call_ended_by_exception(self):
        print('on_call_ended_by_exception')

    def on_return_value(self, return_value_repr):
        print('on_return_value', return_value_repr)

    def on_exception(self, exception):
        print('on_exception', exception)


anitracer = AnimatedTracer()
@anitracer
def bubble_sort(arr):
    for i in range(1, len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
bubble_sort([3,2,1])

# anitracer.render(True)
