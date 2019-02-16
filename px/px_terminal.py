import os
import sys

from . import px_process

if sys.version_info.major >= 3:
    # For mypy PEP-484 static typing validation
    from six import text_type    # NOQA
    from typing import Tuple     # NOQA
    from typing import Optional  # NOQA
    from typing import Iterable  # NOQA

CSI = "\x1b["


def get_window_size():
    # type: () -> Optional[Tuple[int, int]]
    """
    Return the terminal window size as tuple (rows, columns) if available, or
    None if not.
    """

    if not sys.stdout.isatty():
        # We shouldn't truncate lines when piping
        return None

    result = None
    with os.popen('stty size', 'r') as stty_size:
        result = stty_size.read().split()
    if len(result) < 2:
        # Getting the terminal window width failed, don't truncate
        return None

    columns = int(result[1])
    if columns < 1:
        # This seems to happen during OS X CI runs:
        # https://travis-ci.org/walles/px/jobs/113134994
        return None

    rows = int(result[0])
    if rows < 1:
        # Don't know if this actually happens, we just do it for symmetry with
        # the columns check above
        return None

    return (rows, columns)


def to_screen_lines(procs, columns):
    """
    Returns an array of lines that can be printed to screen. Each line is at
    most columns wide.

    If columns is None, line lengths are unbounded.
    """
    class Headings(px_process.PxProcess):
        def __init__(self):
            pass

    headings = Headings()
    headings.pid = "PID"
    headings.command = "COMMAND"
    headings.username = "USERNAME"
    headings.cpu_percent_s = "CPU"
    headings.cpu_time_s = "CPUTIME"
    headings.memory_percent_s = "RAM"
    headings.cmdline = "COMMANDLINE"
    procs = [headings] + procs

    # Compute widest width for pid, command, user, cpu and memory usage columns
    pid_width = 0
    command_width = 0
    username_width = 0
    cpu_width = 0
    cputime_width = 0
    mem_width = 0
    for proc in procs:
        pid_width = max(pid_width, len(str(proc.pid)))
        command_width = max(command_width, len(proc.command))
        username_width = max(username_width, len(proc.username))
        cpu_width = max(cpu_width, len(proc.cpu_percent_s))
        cputime_width = max(cputime_width, len(proc.cpu_time_s))
        mem_width = max(mem_width, len(proc.memory_percent_s))

    format = (
        u'{:>' + str(pid_width) +
        u'} {:' + str(command_width) +
        u'} {:' + str(username_width) +
        u'} {:>' + str(cpu_width) +
        u'} {:>' + str(cputime_width) +
        u'} {:>' + str(mem_width) + u'} {}')

    # Print process list using the computed column widths
    lines = []
    for proc in procs:
        line = format.format(
            proc.pid, proc.command, proc.username,
            proc.cpu_percent_s, proc.cpu_time_s,
            proc.memory_percent_s, proc.cmdline)
        lines.append(line[0:columns])

    return lines


def inverse_video(string):
    # type: (text_type) -> text_type
    CSI = "\x1b["

    return CSI + "7m" + string + CSI + "0m"


def underline_bold(string):
    # type: (text_type) -> text_type
    CSI = "\x1b["

    return CSI + "1;4m" + string + CSI + "0m"


def bold(string):
    # type: (text_type) -> text_type
    CSI = "\x1b["

    return CSI + "1m" + string + CSI + "0m"


def get_string_of_length(string, length):
    # type: (text_type, Optional[int]) -> text_type
    if length is None:
        return string

    if len(string) < length:
        return string + (length - len(string)) * ' '

    if len(string) > length:
        return string[0:length]

    return string


def _tokenize(string):
    # type: (text_type) -> Iterable[text_type]
    """
    Tokenizes string into chars and ANSI sequences.
    """
    i = 0
    while i < len(string):
        try:
            char = string[i]
            if char == CSI[0]:
                c0 = i
                while string[i] != 'm':
                    i += 1
                yield string[c0:i + 1]
                continue

            yield string[i]
        finally:
            i += 1


def crop_ansi_string_at_length(string, length):
    # type: (text_type, int) -> text_type
    result = u""
    char_count = 0
    csi_count = 0

    reset_sequence = u""

    for token in _tokenize(string):
        if char_count == length:
            return result + reset_sequence

        if len(token) == 1:
            char_count += 1
        else:
            csi_count += 1
            reset_sequence = CSI + '0m'

        result += token

    return result + reset_sequence
