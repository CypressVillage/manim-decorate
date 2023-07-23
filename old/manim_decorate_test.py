'''render animations by decoraters'''

from manim import *
from functools import wraps
from collections import UserList

def singleton(cls):
    """单例类装饰器"""
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


class SortAnimateList(UserList):

    def __init__(self, arr_=None):
        self.old = []
        self.new = []
        self.set_arr = []
        super().__init__(arr_)

    def __getitem__(self, item):
        if isinstance(item, slice):
            Sort().construct_fade(Sort.arr[item])
            return super().__getitem__(item)

        self.new.append(item)
        if len(self.new) == 2:
            if set(self.old) != set(self.new):
                Sort.construct_compare(Sort(),self.new[0], self.new[1])
            self.old = self.new
            self.new = []
        return super().__getitem__(item)

    def __setitem__(self, item, val):
        self.set_arr.append(item)
        if len(self.set_arr) == 2:
            Sort.construct_swap(Sort(), self.set_arr[0], self.set_arr[1])
            self.set_arr = []
        return super().__setitem__(item, val)
    

@singleton
class Sort(Scene):
    """render sort functions"""

    auto_play = True

    cmp_color = ORANGE
    origin_color = BLUE
    highlight_color = YELLOW
    bar_color = None

    name = None
    arr = None
    barchart = None
    c_bar_lbls = None
    all_mobject = VGroup() 

    recursion_time = 0


    def set_mode(auto=False, *args, **kwargs):
        Sort.auto_play = auto


    def construct_test(self):
        # self.play(Sort.all_mobject.animate().shift(LEFT+UP))
        ll = 1
        rr = 2

        a = AnimationGroup(*[
            Sort.barchart.bars[i].animate().set_opacity(0.3) for i in range(0, ll)
        ],*[
            Sort.barchart.bars[i].animate().set_opacity(0.3) for i in range(rr+1, len(Sort.arr))
        ])
            
        b = AnimationGroup(*[
            Sort.all_mobject.animate().shift(UP*2+LEFT*4).scale(0.33)
        ])

        self.play(Transform(Sort.all_mobject, Square()))
        self.play(a)
        self.play(b)
        for i in range(rr+1, len(Sort.arr)):
            Sort.barchart.bars[i].set_opacity(0.3)
        for i in range(0,ll):
            Sort.barchart.bars[i].set_opacity(0.3)

    def construct_fade(self, slic):
        left, right = slic[0], slic[len(slic)-1]
        fade = AnimationGroup(*[
            Sort.barchart.bars[i].animate().set_opacity(0.3) for i in range(0, left)
        ],*[
            Sort.barchart.bars[i].animate().set_opacity(0.3) for i in range(right+1, len(Sort.arr))
        ])

        self.play(fade)

        for i in range(0,left):
            Sort.barchart.bars[i].set_opacity(0.3)
        for i in range(right+1, len(Sort.arr)):
            Sort.barchart.bars[i].set_opacity(0.3)

    def construct_sort(self, arr, name):
        Sort.name = Text(name)
        Sort.arr = arr
        Sort.bar_color = [Sort.origin_color for i in range(len(Sort.arr))]
        Sort.barchart = BarChart(
            values=Sort.arr,
            bar_colors=Sort.bar_color,
            bar_fill_opacity=0.5
        )
        Sort.c_bar_lbls = Sort.barchart.get_bar_labels(
            color=Sort.origin_color, label_constructor=MathTex, font_size=36
        )

        Sort.all_mobject.add(
            # Sort.name,
            Sort.barchart,
            Sort.c_bar_lbls
        )

        self.play(Write(Sort.name))
        self.play(Unwrite(Sort.name, reverse=False))
        self.play(Create(Sort.barchart))
        self.play(Create(Sort.c_bar_lbls))

    def construct_swap(self, index_a, index_b):
        swap_bar = AnimationGroup(*[
            Sort.barchart.bars[index_a].animate().shift(RIGHT*(Sort.barchart.bars[index_b].get_x()-Sort.barchart.bars[index_a].get_x())),
            Sort.barchart.bars[index_b].animate().shift(LEFT*(Sort.barchart.bars[index_b].get_x()-Sort.barchart.bars[index_a].get_x())),
            Sort.c_bar_lbls[index_a].animate().shift(RIGHT*(Sort.barchart.bars[index_b].get_x()-Sort.barchart.bars[index_a].get_x())),
            Sort.c_bar_lbls[index_b].animate().shift(LEFT*(Sort.barchart.bars[index_b].get_x()-Sort.barchart.bars[index_a].get_x()))
        ])
        self.play(swap_bar)
        Sort.barchart.bars[index_a], Sort.barchart.bars[index_b] = Sort.barchart.bars[index_b], Sort.barchart.bars[index_a]
        Sort.c_bar_lbls[index_a], Sort.c_bar_lbls[index_b] = Sort.c_bar_lbls[index_b], Sort.c_bar_lbls[index_a]

    def construct_compare(self, index_a, index_b):
        pre_color_a = Sort.barchart.bars[index_a].get_color()
        pre_color_b = Sort.barchart.bars[index_b].get_color()
        highlight_bar = AnimationGroup(*[
            FadeToColor(Sort.barchart.bars[index_a], color=Sort.cmp_color),
            FadeToColor(Sort.barchart.bars[index_b], color=Sort.cmp_color),
            FadeToColor(Sort.c_bar_lbls[index_a], color=Sort.cmp_color),
            FadeToColor(Sort.c_bar_lbls[index_b], color=Sort.cmp_color)
        ])
        dehighlight_bar = AnimationGroup(*[
            FadeToColor(Sort.barchart.bars[index_a], color=pre_color_a),
            FadeToColor(Sort.barchart.bars[index_b], color=pre_color_b),
            FadeToColor(Sort.c_bar_lbls[index_a], color=pre_color_a),
            FadeToColor(Sort.c_bar_lbls[index_b], color=pre_color_b)
        ])
        self.play(highlight_bar)
        self.play(dehighlight_bar)

    def construct_frame(self, index_a, index_b):
        frame = Rectangle()

        self.play(Create(frame))
        self.play(Uncreate(frame))


    def construct_highlight(self):
        pass

    def sort(name='Sort Animation'):
        def sort_(func):
            @wraps(func)
            def wrapper(arr, *args, **kwargs):

                Sort().construct_sort(arr)
                returnVal = func(arr, *args, **kwargs)
                Sort().render(Sort.auto_play)
                Sort().clear()

                return returnVal
            return wrapper
        return sort_

    def compare(func):
        @wraps(func)
        def wrapper(index_a, index_b):

            Sort().construct_compare(index_a, index_b)
            if Sort.arr[index_a] > Sort.arr[index_b]:
                return True
            return False

        return wrapper

    def swap(func):
        @wraps(func)
        def wrapper(index_a, index_b):

            Sort().construct_swap(index_a, index_b)
            Sort.arr[index_a], Sort.arr[index_b] = Sort.arr[index_b], Sort.arr[index_a]
            return Sort.arr

        return wrapper

    def auto(name='Sort Animation'):
        def auto_(func):
            @wraps(func)
            def wrapper(arr, *args, **kwargs):
                
                if Sort.recursion_time == 0:
                    Sort().construct_sort(arr, name)
                Sort.recursion_time += 1
                returnVal = func(SortAnimateList(arr), *args, **kwargs)
                Sort.recursion_time -= 1
                if Sort.recursion_time == 0:
                    Sort().render(Sort.auto_play)
                    Sort().clear()

                return returnVal
            return wrapper
        return auto_