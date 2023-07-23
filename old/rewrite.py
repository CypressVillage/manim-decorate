import pysnooper
from rich import print, inspect

class Tracer(pysnooper.snoop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.oldwrite = self.write

    def write(self, s):
        self.oldwrite(s)

        