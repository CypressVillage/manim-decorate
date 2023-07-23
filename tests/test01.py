
import manim_decorate_test as md
from loguru import logger
import pysnooper

# pysnooper.tracer.DISABLED = True

# @logger.catch
# @pysnooper.snoop()

@md.Sort.auto()
def mergeSort(arr):
    if len(arr) < 2:
        return arr
    middle = len(arr)//2
    return merge(mergeSort(arr[0:middle]), mergeSort(arr[middle:]))

@md.Sort.auto()
def merge(arr1, arr2):
    ans = []
    while arr1 and arr2:
        if arr1[0] < arr2[0]:
            ans.append(arr1[0])
            arr1.pop(0)
        else:
            ans.append(arr2[0])
            arr2.pop(0)
    while arr1:
        ans.append(arr1[0])
        arr1.pop(0)

    while arr2:
        ans.append(arr2[0])
        arr2.pop(0)
    return ans


mergeSort([3,2,1])


# @pysnooper.snoop()
# def bubble_sort(arr):
#     for i in range(1, len(arr)):
#         for j in range(0, len(arr)-i):
#             if arr[j] > arr[j+1]:
#                 arr[j], arr[j+1] = arr[j+1], arr[j]
#     return arr
# bubble_sort([6,5,4,3,2,1])
