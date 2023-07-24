import sys
from pysnooper.tracer import Tracer as pytracer # 以后改成自己的tracer
import Scene as Scene_
from manimtracer import manimtrace
import inspect
# from rich import print, inspect

class Tracer(pytracer):
    def __init__(self, scene:str="Basic", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = self.color or sys.platform in ('win32',)

        self._trace = self.trace
        self.trace = self._scene_trace

        self.scene = scene
        self.painter = getattr(Scene_, scene)()

        self.write = lambda s: None

    def _scene_trace(self, frame, event, arg):
        # rtn = self._trace(frame, event, arg)
        # if rtn is not None:
        #     self.painter.construct(frame, event, arg)
        rtn = manimtrace(self, frame, event, arg, self.painter)
        return rtn

tra = Tracer('Sort', color=True)
@tra
def bubble_sort(arr):
    for i in range(1, len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

bubble_sort([3,2,1])

tra.painter.render(True)
