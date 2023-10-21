这里存放之前用装饰器实现的版本

- `README.md`: 本文件
- `learn_snooper.py`: 对 `pysnooper` 库进行了注释
- `manim_decorator.py`: 装饰器实现的版本
- `manim_decorator_test.py`: 一些测试功能，可能存在 bug
- `bubbleSort_test.py`: 冒泡排序渲染测试

## Manim Decorate

使用装饰器轻松渲染你写出的排序算法

本项目基于 Manim 动画库，将渲染动画的部分集成到装饰器中。用户只需要关心自身算法的实现，调用装饰器即可一键渲染动画。

目前仅支持交换类排序算法

## 用法示例

基本用法：在排序算法函数前添加装饰器 `@md.Sort.auto('动画名')`

运行函数即可生成动画
```python
import manim_decorate as md

@md.Sort.auto('bubble sort')
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-1, i, -1):
            if arr[j] < arr[j-1]:
                arr[j], arr[j-1] = arr[j-1], arr[j]

bubble_sort([1, 3, 2, 4])
```
效果如下：

<video src="Sort.mp4" controls title="Title"></video>

如果想自定义动画，可以添加 `swap`、`compare` 等装饰器自定义动画细节

```python
import manim_decorate as md

@md.Sort.compare()
def cmp(a, b):
    if a < b:
        return True
    return False

@md.Sort.sort('自定义装饰器')
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-1, i, -1):
            if cmp(arr[j], arr[j-1]):
                arr[j], arr[j-1] = arr[j-1], arr[j]

bubble_sort([1, 3, 2, 4])
```