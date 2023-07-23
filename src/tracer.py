import sys
import pysnooper
from rich import print, inspect
import Scene

class Tracer(pysnooper.snoop):
    def __init__(self, scene:str="Basic", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = self.color or sys.platform in ('win32',)

        self._trace = self.trace
        self.trace = self._scene_trace

        self.scene = scene
        self.painter = getattr(Scene, scene)()

    def _scene_trace(self, frame, event, arg):
        rtn = self._trace(frame, event, arg)
        if rtn is not None:
            self.painter.construct(frame, event, arg)
        return rtn
    

@Tracer('Basic', color=True, prefix='[bold red]')
def bubble_sort(arr):
    for i in range(1, len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

bubble_sort([6,5,4,3,2,1])
