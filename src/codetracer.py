from collections import namedtuple
from typing import List
from inspect import getsourcelines

# from rich import inspect
from manim import *
from colour import Color

from animatedtracer import AnimatedTracer

Codeline = namedtuple('Codeline', ['line_no', 'source_line', 'text_obj'])

class CodeTracer(AnimatedTracer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.linenums: List[int] = []
        self.sources: List[str] = []
        self.textobjs: List[Text] = []

        self.focusline: Rectangle

    def __call__(self, function_or_class):
        self.construct_generate_code(function_or_class)
        return super().__call__(function_or_class)

    def on_elapsed_time(self, start_time, elapsed_time_string):
        print('on_elapsed_time', start_time, elapsed_time_string)

    def on_source_path(self, source_path):
        pass

    def on_newish_variable(self, newish_string, name, value_repr):
        pass

    def on_modified_variable(self, name, value_repr):
        pass

    def on_finished_line(self, indent, timestamp, thread_info, event, line_no, source_line):
        self.construct_focusline(line_no)

    def on_call_ended_by_exception(self):
        pass

    def on_return_value(self, return_value_repr):
        pass

    def on_exception(self, exception):
        pass

    def construct_generate_code(self, function_or_class):
        source, firstline = getsourcelines(function_or_class)
        for dx, source_line in enumerate(source):
            self.linenums.append(firstline+dx)
            self.sources.append(source_line)
            self.construct_newline(firstline+dx, source_line)

    def construct_newline(self, line_no: int, source_line: str):
        text = Text(str(line_no)+'  '+source_line, font="Consolas", font_size=25, t2c={"def": YELLOW_D})
        self.textobjs.append(text)

        delta_index = line_no - min(self.linenums)
        text.to_corner(UL).shift(DOWN*delta_index/2)

        self.add(self.textobjs[-1])
        self.play(Write(self.textobjs[-1]))

    def construct_focusline(self, line_no: int):
        index = self.linenums.index(line_no)
        if not hasattr(self, 'focusline'):
            self.focusline = Rectangle(height=0.5, width=30, color=Color(YELLOW_C), fill_opacity=0.3).move_to(self.textobjs[index])
            self.play(Create(self.focusline))
        else:
            self.play(self.focusline.animate.move_to(self.textobjs[index]))

tracer = CodeTracer()
tracer2 = CodeTracer()
# tracer = AnimatedTracer()

@tracer
class BubbleSort:
    def sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]

    def aaa(self):
        pass

arr = [64, 34, 25]

BubbleSort().aaa()
BubbleSort().sort(arr)
tracer.render(True)