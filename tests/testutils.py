import re
import random
import datetime

from px import px_file
from px import px_process
from px import px_ipc_map

import dateutil.tz
import dateutil.parser


import sys
if sys.version_info.major >= 3:
    # For mypy PEP-484 static typing validation
    from typing import MutableMapping  # NOQA


# An example time string that can be produced by ps
TIMESTRING = "Mon Mar 7 09:33:11 2016"
TIME = dateutil.parser.parse(TIMESTRING).replace(tzinfo=dateutil.tz.tzlocal())


def spaces(at_least=1, at_most=3):
    return " " * random.randint(at_least, at_most)


def now():
    return datetime.datetime.now().replace(tzinfo=dateutil.tz.tzlocal())


def create_process(pid=47536, ppid=1234,
                   timestring=TIMESTRING,
                   username="root",
                   cputime="0:00.03", mempercent="0.0",
                   commandline="/usr/sbin/cupsd -l",
                   now=now()):

    psline = (spaces(at_least=0) +
              str(pid) + spaces() +
              str(ppid) + spaces() +
              timestring + spaces() +
              username + spaces() +
              cputime + spaces() +
              mempercent + spaces() +
              commandline)

    return px_process.ps_line_to_process(psline, now)


def create_file(filetype, name, device, pid, access=None, inode=None):
    file = px_file.PxFile()
    file.type = filetype

    # Remove leading [] group from name if any
    file.name = re.match('(\[[^]]*\] )?(.*)', name).group(2)

    file.pid = pid
    file.device = device
    file.access = access
    file.inode = inode
    return file


def create_ipc_map(pid, all_files):
    """Wrapper around IpcMap() so that we can test it"""
    pid2process = {}  # type: MutableMapping[int, px_process.PxProcess]
    for file in all_files:
        if file.pid in pid2process:
            continue
        pid2process[file.pid] = create_process(pid=file.pid)
    if pid not in pid2process:
        pid2process[pid] = create_process(pid=pid)

    processes = list(pid2process.values())
    random.shuffle(processes)

    process = pid2process[pid]

    return px_ipc_map.IpcMap(process, all_files, processes)
