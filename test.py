
import manim_decorate as md

@md.Sort.auto('shell sort')
def shell_sort(arr):
    h = 1
    length = len(arr)
    while h < length / 3:
        h = int(3 * h + 1)
    while h >= 1:
        for i in range(h, length):
            j = i
            while j >= h and arr[j-h] > arr[j]:
                arr[j], arr[j-h] = arr[j-h], arr[j]
                j -= h
        h = int(h / 3)

@md.Sort.auto('bubble sort')
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-1, i, -1):
            if arr[j] < arr[j-1]:
                arr[j], arr[j-1] = arr[j-1], arr[j]

@md.Sort.auto('selection sort')
def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

@md.Sort.auto('insertion sort')
def insertion_sort(arr):
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            if arr[j] < arr[j-1]:
                arr[j], arr[j-1] = arr[j-1], arr[j]

bubble_sort([1, 3, 2, 4])