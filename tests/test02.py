'''test animations'''

import manim_decorate_test as md

ss = md.Sort()
ss.construct_sort([1,2,3,4,5], 'animate test')

ss.construct_test()

ss.render(True)