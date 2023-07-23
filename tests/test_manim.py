from manim import *

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen

class Anim01(Scene):
    def construct(self):
        self.play(Write(Text("Hello World")))
        # return super().construct()
    
a01 = Anim01()
a01.construct()
a01.render(True)