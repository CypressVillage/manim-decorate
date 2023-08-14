from manim import *
from manim_data_structures import *
from basic_tracer import BasicTracer

class MemoryTracer(BasicTracer):
    def __init__(self, tracer):
        super().__init__(tracer)
        self.memory = []

class TestMemory(Scene):
    def __init__(self):
        super().__init__()
        self.width = 1
        self.height = 1

    def construct_init(self):
        var = MVariable(Scene, '11', 1, 'label')
        self.add(var)
        rec = Rectangle(width=self.width, height=self.height)
        self.play(Create(rec))
        self.play(rec.animate.shift(UP))

    def construct_new_var(self, var_name, var_value, var_type):
        pass

    def construct_malloc(self):
        pass

test = TestMemory()
test.construct_init()
test.render(True)