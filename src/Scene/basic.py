from manim import Scene

class Basic(Scene):
    def construct(self, frame, event, arg):
        if event == 'call':
            self.construct_call()
        elif event == 'line':
            self.construct_line()
        elif event == 'return':
            self.construct_return()
        elif event == 'exception':
            self.construct_exception()

    def construct_call(self):
        print("__call__")

    def construct_line(self):
        print("__line__")

    def construct_event(self):
        print("__event__")

    def construct_exception(self):
        print("__exception__")

    def construct_return(self):
        print("__return__")

