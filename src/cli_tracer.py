from basic_tracer import BasicTracer

class CLITracer(BasicTracer):
    def on_elapsed_time(self, start_time, elapsed_time_string):
        print('on_elapsed_time___________', start_time, elapsed_time_string)

    def on_source_path(self, source_path):
        print('on_source_path____________', source_path)

    def on_newish_variable(self, newish_string, name, value_repr):
        print('on_newish_variable________', newish_string, name, value_repr)

    def on_modified_variable(self, name, value_repr):
        print('on_modified_variable______', name, value_repr)

    def on_finished_line(self, indent, timestamp, thread_info, event, line_no, source_line):
        print('on_finished_line__________', timestamp, thread_info, event, line_no, source_line)

    def on_call_ended_by_exception(self):
        print('on_call_ended_by_exception')

    def on_return_value(self, return_value_repr):
        print('on_return_value___________', return_value_repr)

    def on_exception(self, exception):
        print('on_exception______________', exception)
