from manimdecorate import cli_tracer
from manimdecorate import sortFn_tracer
# from manim_decorate import Sort


# @cli_tracer.CLITracer()
@sortFn_tracer.sortFn_tracer()
# @Sort.sort('dasd')
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

@sortFn_tracer.sortFn_tracer()
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

array = [64, 34, 25, 12, 22, 11, 90]
selection_sort(array)
