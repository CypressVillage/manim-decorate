from snooper import snoop as snooptracer  # 以后改成自己的tracer
from manim import Scene

class BasicTracer(snooptracer, Scene):
    def __init__(self, *args, **kwargs):
        snooptracer.__init__(self, *args, **kwargs)
        Scene.__init__(self)
        # self.color = self.color or sys.platform in ('win32',)
        self.write = lambda s: None

    def on_elapsed_time(self, start_time, elapsed_time_string):
        pass

    def on_source_path(self, source_path):
        pass

    def on_newish_variable(self, newish_string, name, value_repr):
        pass

    def on_modified_variable(self, name, value_repr):
        pass

    def on_finished_line(self, indent, timestamp, thread_info, event, line_no, source_line):
        pass

    def on_call_ended_by_exception(self):
        pass

    def on_return_value(self, return_value_repr):
        pass

    def on_exception(self, exception):
        pass
