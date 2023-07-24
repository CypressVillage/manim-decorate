from manim import Scene

class Basic(Scene):
    # def construct(self, frame, event, arg):
    #     if event == 'call':
    #         self.construct_call()
    #     elif event == 'line':
    #         self.construct_line()
    #     elif event == 'return':
    #         self.construct_return()
    #     elif event == 'exception':
    #         self.construct_exception()

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

    def on_source_path(self):
        pass

    def on_newish_variable(self, variable_name, variable_value):
        print(f"New variable: {variable_name} = {variable_value}")

    def on_modified_variable(self, variable_name, variable_value):
        print(f"Modified variable: {variable_name} = {variable_value}")

    def on_call_ended_by_exception(self):
        pass

    def on_line_no(self):
        pass

    def on_return_value(self, return_value):
        print(f"Return value: {return_value}")
