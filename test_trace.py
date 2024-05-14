from manimdecorate import cli_tracer
from manimdecorate import sortFn_tracer
from manim_decorate import Sort


# @cli_tracer.CLITracer()
@sortFn_tracer.sortFn_tracer()
# @Sort.sort('dasd')
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

array = [64, 34, 25, 12, 22, 11, 90]
bubble_sort(array)
