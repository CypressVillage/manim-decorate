from .basic_tracer import BasicTracer
from manim import *

class sortFn_tracer(BasicTracer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.auto_play = True
        self.list_created = False

        self.cmp_color = ORANGE
        self.origin_color = BLUE
        self.highlight_color = YELLOW
        self.bar_color = None

        self.name = None
        self.arr = None
        self.arr_name = None
        self.barchart = None
        self.c_bar_lbls = None

    def construct_sort(self, arr, name):
        self.name = Text(name)
        self.arr = arr
        self.bar_color = [self.origin_color for i in range(len(self.arr))]
        self.barchart = BarChart(
            values=self.arr,
            bar_colors=self.bar_color,
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
        swap_bar = AnimationGroup(*[
            self.barchart.bars[index_a].animate().shift(RIGHT*(self.barchart.bars[index_b].get_x()-self.barchart.bars[index_a].get_x())),
            self.barchart.bars[index_b].animate().shift(LEFT*(self.barchart.bars[index_b].get_x()-self.barchart.bars[index_a].get_x())),
            self.c_bar_lbls[index_a].animate().shift(RIGHT*(self.barchart.bars[index_b].get_x()-self.barchart.bars[index_a].get_x())),
            self.c_bar_lbls[index_b].animate().shift(LEFT*(self.barchart.bars[index_b].get_x()-self.barchart.bars[index_a].get_x()))
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


    def construct_highlight(self):
        pass

    def on_newish_variable(self, newish_string, name, value_repr):
        if 'Starting var' in newish_string and not self.list_created:
            print('constructing sort')
            self.name = 'Array'
            self.list_created = True
            value_repr = [int(i) for i in value_repr[1:-1].split(', ')]
            self.arr = value_repr
            self.arr_name = name
            self.construct_sort(value_repr, self.name)

    def on_modified_variable(self, name, value_repr):
        if name == self.arr_name:
            value_repr = [int(i) for i in value_repr[1:-1].split(', ')]
            # find the index of the two elements to be swapped
            idx = [i for i, [a, b] in enumerate(zip(self.arr, value_repr)) if a != b]
            print('swapping', idx)
            if len(idx) != 2:
                return
            idx_a, idx_b = idx[0], idx[1]
            self.construct_swap(idx_a, idx_b)
            self.arr = value_repr

    def on_return_value(self, return_value_repr):
        self.render(self.auto_play)