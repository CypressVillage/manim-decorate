from manim_decorate import Sort

@Sort.auto('Bubble Sort')
def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

a = bubbleSort([1, 4, 3, 2, 5])