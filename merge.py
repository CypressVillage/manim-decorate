import loguru
import pysnooper
from colorama import init
init()
@pysnooper.snoop(color=True)
@loguru.logger.catch
def mergeSort(arr):
    if len(arr) < 2:
        return arr

    middle = len(arr)//2
    return merge(mergeSort(arr[0:middle]), mergeSort(arr[middle:]))

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



n = int(input())
for i in range(n):
    in_li = list(map(int,input().split(' ')))
    print(mergeSort(in_li))