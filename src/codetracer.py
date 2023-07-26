from typing import List
from inspect import getsourcelines, currentframe

from manim import *
from colour import Color

from codestyle import Codestyle
from animatedtracer import AnimatedTracer

class CodeTracer(AnimatedTracer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.codestyle = Codestyle
        self.scale = 0.5

        self.linenums: List[int] = []
        self.sources: List[str] = []
        self.textobjs: List[Text] = []

        self.focusline: Rectangle

    def __call__(self, function_or_class):
        self.construct_generate_code(function_or_class)
        return super().__call__(function_or_class)

    # def __enter__(self):
    # #     frame = currentframe()
    # #     print(frame.f_back)
    # #     self.construct_generate_code(frame.f_back)
    #     super().__enter__()
    #     return self

    # def __exit__(self, exc_type, exc_value, traceback):
    #     super().__exit__(exc_type, exc_value, traceback)
    #     return self

    def on_elapsed_time(self, start_time, elapsed_time_string):
        super().on_elapsed_time(start_time, elapsed_time_string)

    def on_source_path(self, source_path):
        pass

    def on_newish_variable(self, newish_string, name, value_repr):
        pass

    def on_modified_variable(self, name, value_repr):
        pass

    def on_finished_line(self, indent, timestamp, thread_info, event, line_no, source_line):
        if line_no not in self.linenums:
            self.add_new_line(line_no, source_line)
        self.construct_focusline(line_no)

    def on_call_ended_by_exception(self):
        pass

    def on_return_value(self, return_value_repr):
        pass

    def on_exception(self, exception):
        pass

    def add_new_line(self, line_no: int, source_line: str):
        self.linenums.append(line_no)
        self.sources.append(source_line)
        self.construct_newline(line_no, source_line)

    def construct_generate_code(self, function_or_class):
        source, firstline = getsourcelines(function_or_class)
        for dx, source_line in enumerate(source):
            self.add_new_line(firstline+dx, source_line)

    def construct_newline(self, line_no: int, source_line: str):
        text = Text(str(line_no)+'  '+source_line, font="Consolas", font_size=25, t2c=self.codestyle)
        self.textobjs.append(text)

        if self.linenums:
            delta_index = line_no - min(self.linenums)
        else:
            delta_index = 0
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
def fib(n):
        if n <= 1:
            return n
        else:
            return fib(n-1) + fib(n-2)

fib(5)
tracer.render(True)