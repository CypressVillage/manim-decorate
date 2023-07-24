from manim import *
from .basic import Basic

class Sort(Basic):
    def on_newish_variable(self, variable_name, variable_value):
        pass

    def on_modified_variable(self, variable_name, variable_value):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen