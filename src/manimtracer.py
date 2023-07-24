import functools
import inspect
import opcode
import os
import sys
import re
import collections
import datetime as datetime_module
import itertools
import threading
import traceback

from pysnooper.variables import CommonVariable, Exploding, BaseVariable
from pysnooper import utils, pycompat
if pycompat.PY2:
    from io import open


def get_local_reprs(frame, watch=(), custom_repr=(), max_length=None, normalize=False):
    code = frame.f_code
    vars_order = (code.co_varnames + code.co_cellvars + code.co_freevars +
                  tuple(frame.f_locals.keys()))

    result_items = [(key, utils.get_shortish_repr(value, custom_repr,
                                                  max_length, normalize))
                    for key, value in frame.f_locals.items()]
    result_items.sort(key=lambda key_value: vars_order.index(key_value[0]))
    result = collections.OrderedDict(result_items)

    for variable in watch:
        result.update(sorted(variable.items(frame, normalize)))
    return result


source_and_path_cache = {}
def get_path_and_source_from_frame(frame):
    globs = frame.f_globals or {}
    module_name = globs.get('__name__')
    file_name = frame.f_code.co_filename
    cache_key = (module_name, file_name)
    try:
        return source_and_path_cache[cache_key]
    except KeyError:
        pass
    loader = globs.get('__loader__')

    source = None
    if hasattr(loader, 'get_source'):
        try:
            source = loader.get_source(module_name)
        except ImportError:
            pass
        if source is not None:
            source = source.splitlines()
    if source is None:
        ipython_filename_match = ipython_filename_pattern.match(file_name)
        ansible_filename_match = ansible_filename_pattern.match(file_name)
        if ipython_filename_match:
            entry_number = int(ipython_filename_match.group(1))
            try:
                import IPython
                ipython_shell = IPython.get_ipython()
                ((_, _, source_chunk),) = ipython_shell.history_manager. \
                                  get_range(0, entry_number, entry_number + 1)
                source = source_chunk.splitlines()
            except Exception:
                pass
        elif ansible_filename_match:
            try:
                import zipfile
                archive_file = zipfile.ZipFile(ansible_filename_match.group(1), 'r')
                source = archive_file.read(ansible_filename_match.group(2).replace('\\', '/')).splitlines()
            except Exception:
                pass
        else:
            try:
                with open(file_name, 'rb') as fp:
                    source = fp.read().splitlines()
            except utils.file_reading_errors:
                pass
    if not source:
        # We used to check `if source is None` but I found a rare bug where it
        # was empty, but not `None`, so now we check `if not source`.
        source = UnavailableSource()

    # If we just read the source from a file, or if the loader did not
    # apply tokenize.detect_encoding to decode the source into a
    # string, then we should do that ourselves.
    if isinstance(source[0], bytes):
        encoding = 'utf-8'
        for line in source[:2]:
            # File coding may be specified. Match pattern from PEP-263
            # (https://www.python.org/dev/peps/pep-0263/)
            match = re.search(br'coding[:=]\s*([-\w.]+)', line)
            if match:
                encoding = match.group(1).decode('ascii')
                break
        source = [pycompat.text_type(sline, encoding, 'replace') for sline in
                  source]

    result = (file_name, source)
    source_and_path_cache[cache_key] = result
    return result

thread_global = threading.local()
DISABLED = bool(os.getenv('PYSNOOPER_DISABLED', ''))

thread_global.__dict__.setdefault('depth', -1)
# calling_frame = inspect.currentframe().f_back

def manimtrace(self, frame, event, arg, painter):
    ### Checking whether we should trace this line: #######################
    #                                                                     #
    # We should trace this line either if it's in the decorated function,
    # or the user asked to go a few levels deeper and we're within that
    # number of levels deeper.
    '''
    if not (frame.f_code in self.target_codes or frame in self.target_frames):
        if self.depth == 1:
            # We did the most common and quickest check above, because the
            # trace function runs so incredibly often, therefore it's
            # crucial to hyper-optimize it for the common case.
            return None
        elif self._is_internal_frame(frame):
            return None
        else:
            _frame_candidate = frame
            for i in range(1, self.depth):
                _frame_candidate = _frame_candidate.f_back
                if _frame_candidate is None:
                    return None
                elif _frame_candidate.f_code in self.target_codes or _frame_candidate in selftarget_frames:
                    break
            else:
                return None
    #                                                                     #
    ### Finished checking whether we should trace this line. ##############
    '''

    if event == 'call':
        thread_global.depth += 1
    indent = ' ' * 4 * thread_global.depth
    _FOREGROUND_BLUE = self._FOREGROUND_BLUE
    _FOREGROUND_CYAN = self._FOREGROUND_CYAN
    _FOREGROUND_GREEN = self._FOREGROUND_GREEN
    _FOREGROUND_MAGENTA = self._FOREGROUND_MAGENTA
    _FOREGROUND_RED = self._FOREGROUND_RED
    _FOREGROUND_RESET = self._FOREGROUND_RESET
    _FOREGROUND_YELLOW = self._FOREGROUND_YELLOW
    _STYLE_BRIGHT = self._STYLE_BRIGHT
    _STYLE_DIM = self._STYLE_DIM
    _STYLE_NORMAL = self._STYLE_NORMAL
    _STYLE_RESET_ALL = self._STYLE_RESET_ALL
    ### Making timestamp: #################################################
    #                                                                     #
    if self.normalize:
        timestamp = ' ' * 15
    elif self.relative_time:
        try:
            start_time = self.start_times[frame]
        except KeyError:
            start_time = self.start_times[frame] = \
                                             datetime_module.datetime.now()
        duration = datetime_module.datetime.now() - start_time
        timestamp = pycompat.timedelta_format(duration)
    else:
        timestamp = pycompat.time_isoformat(
            datetime_module.datetime.now().time(),
            timespec='microseconds'
        )
    #                                                                     #
    ### Finished making timestamp. ########################################

    line_no = frame.f_lineno
    source_path, source = get_path_and_source_from_frame(frame)
    source_path = source_path if not self.normalize else os.path.basename(source_path)
    if self.last_source_path != source_path:
        self.write(u'{_FOREGROUND_YELLOW}{_STYLE_DIM}{indent}Source path:... '
                   u'{_STYLE_NORMAL}{source_path}'
                   u'{_STYLE_RESET_ALL}'.format(**locals()))
        painter.on_source_path()
        self.last_source_path = source_path
    source_line = source[line_no - 1]
    thread_info = ""
    if self.thread_info:
        if self.normalize:
            raise NotImplementedError("normalize is not supported with "
                                      "thread_info")
        current_thread = threading.current_thread()
        thread_info = "{ident}-{name} ".format(
            ident=current_thread.ident, name=current_thread.getName())
    thread_info = self.set_thread_info_padding(thread_info)
    ### Reporting newish and modified variables: ##########################
    #                                                                     #
    old_local_reprs = self.frame_to_local_reprs.get(frame, {})
    self.frame_to_local_reprs[frame] = local_reprs = \
                                   get_local_reprs(frame,
                                                   watch=self.watch, custom_repr=self.custom_repr,
                                                   max_length=self.max_variable_length,
                                                   normalize=self.normalize,
                                                   )
    newish_string = ('Starting var:.. ' if event == 'call' else
                                                        'New var:....... ')
    for name, value_repr in local_reprs.items():
        if name not in old_local_reprs:
            self.write('{indent}{_FOREGROUND_GREEN}{_STYLE_DIM}'
                       '{newish_string}{_STYLE_NORMAL}{name} = '
                       '{value_repr}{_STYLE_RESET_ALL}'.format(**locals()))
            painter.on_newish_variable(name, value_repr)
        elif old_local_reprs[name] != value_repr:
            self.write('{indent}{_FOREGROUND_GREEN}{_STYLE_DIM}'
                       'Modified var:.. {_STYLE_NORMAL}{name} = '
                       '{value_repr}{_STYLE_RESET_ALL}'.format(**locals()))
            painter.on_modified_variable(name, value_repr)
    #                                                                     #
    ### Finished newish and modified variables. ###########################
    ### Dealing with misplaced function definition: #######################
    #                                                                     #
    if event == 'call' and source_line.lstrip().startswith('@'):
        # If a function decorator is found, skip lines until an actual
        # function definition is found.
        for candidate_line_no in itertools.count(line_no):
            try:
                candidate_source_line = source[candidate_line_no - 1]
            except IndexError:
                # End of source file reached without finding a function
                # definition. Fall back to original source line.
                break
            if candidate_source_line.lstrip().startswith('def'):
                # Found the def line!
                line_no = candidate_line_no
                source_line = candidate_source_line
                break
    #                                                                     #
    ### Finished dealing with misplaced function definition. ##############
    # If a call ends due to an exception, we still get a 'return' event
    # with arg = None. This seems to be the only way to tell the difference
    # https://stackoverflow.com/a/12800909/2482744
    code_byte = frame.f_code.co_code[frame.f_lasti]
    if not isinstance(code_byte, int):
        code_byte = ord(code_byte)
    ended_by_exception = (
            event == 'return'
            and arg is None
            and (opcode.opname[code_byte]
                 not in ('RETURN_VALUE', 'YIELD_VALUE'))
    )
    if ended_by_exception:
        self.write('{_FOREGROUND_RED}{indent}Call ended by exception{_STYLE_RESET_ALL}'.
                   format(**locals()))
        painter.on_call_ended_by_exception()
    else:
        self.write(u'{indent}{_STYLE_DIM}{timestamp} {thread_info}{event:9} '
                   u'{line_no:4}{_STYLE_RESET_ALL} {source_line}'.format(**locals()))
        painter.on_line_no()
    if event == 'return':
        self.frame_to_local_reprs.pop(frame, None)
        self.start_times.pop(frame, None)
        thread_global.depth -= 1
        if not ended_by_exception:
            return_value_repr = utils.get_shortish_repr(arg,
                                                        custom_repr=self.custom_repr,
                                                        max_length=self.max_variable_length,
                                                        normalize=self.normalize,
                                                        )
            self.write('{indent}{_FOREGROUND_CYAN}{_STYLE_DIM}'
                       'Return value:.. {_STYLE_NORMAL}{return_value_repr}'
                       '{_STYLE_RESET_ALL}'.
                       format(**locals()))
            painter.on_return_value(return_value_repr)
    if event == 'exception':
        exception = '\n'.join(traceback.format_exception_only(*arg[:2])).strip()
        if self.max_variable_length:
            exception = utils.truncate(exception, self.max_variable_length)
        self.write('{indent}{_FOREGROUND_RED}Exception:..... '
                   '{_STYLE_BRIGHT}{exception}'
                   '{_STYLE_RESET_ALL}'.format(**locals()))
    return self.trace