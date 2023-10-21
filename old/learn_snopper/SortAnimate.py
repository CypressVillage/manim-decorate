
from manim import *
        
class Sort(Scene):
    """render sort functions"""

    def __init__(self):
        super().__init__()

        self.auto_play = True
        self.origin_color = BLUE
        self.cmp_color = ORANGE
        self.highlight_color = YELLOW
        self.bar_colors = None
        self.name = None
        self.arr = None
        self.barchart = None
        self.c_bar_lbls = None


    def set_mode(self, auto_play=True, cmp_color = ORANGE, ):
        self.auto_play = auto_play


    def construct_sort(self, arr, name='Sort Animation'):
        self.name = Text(name)
        self.arr = arr
        self.bar_colors = [self.origin_color]*len(self.arr)
        self.barchart = BarChart(
            values=self.arr,
            bar_colors=self.bar_colors,
            bar_fill_opacity=0.5
        )
        self.c_bar_lbls = self.barchart.get_bar_labels(
            color=self.origin_color, label_constructor=MathTex, font_size=36
        )

        self.play(Write(self.name))
        self.play(Unwrite(self.name, reverse=False))
        self.play(Create(self.barchart))
        self.play(Create(self.c_bar_lbls))

    def construct_swap(self, index_a, index_b):
        dist = self.barchart.bars[index_b].get_x()-self.barchart.bars[index_a].get_x()
        swap_bar = AnimationGroup(*[
            self.barchart.bars[index_a].animate().shift(RIGHT*dist),
            self.barchart.bars[index_b].animate().shift(LEFT*dist),
            self.c_bar_lbls[index_a].animate().shift(RIGHT*dist),
            self.c_bar_lbls[index_b].animate().shift(LEFT*dist)
        ])
        self.play(swap_bar)
        self.barchart.bars[index_a], self.barchart.bars[index_b] = self.barchart.bars[index_b], self.barchart.bars[index_a]
        self.c_bar_lbls[index_a], self.c_bar_lbls[index_b] = self.c_bar_lbls[index_b], self.c_bar_lbls[index_a]

    def construct_compare(self, index_a, index_b):
        pre_color_a = self.barchart.bars[index_a].get_color()
        pre_color_b = self.barchart.bars[index_b].get_color()
        highlight_bar = AnimationGroup(*[
            FadeToColor(self.barchart.bars[index_a], color=self.cmp_color),
            FadeToColor(self.barchart.bars[index_b], color=self.cmp_color),
            FadeToColor(self.c_bar_lbls[index_a], color=self.cmp_color),
            FadeToColor(self.c_bar_lbls[index_b], color=self.cmp_color)
        ])
        dehighlight_bar = AnimationGroup(*[
            FadeToColor(self.barchart.bars[index_a], color=pre_color_a),
            FadeToColor(self.barchart.bars[index_b], color=pre_color_b),
            FadeToColor(self.c_bar_lbls[index_a], color=pre_color_a),
            FadeToColor(self.c_bar_lbls[index_b], color=pre_color_b)
        ])
        self.play(highlight_bar)
        self.play(dehighlight_bar)


    def construct_highlight(self, index):
        pass
