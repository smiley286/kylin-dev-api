#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import locale
from utils.enums import *


class Worker():

    def __init__(self, dbusDaemon):
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
        self.dbusDaemon = dbusDaemon

    # 执行本地命令
    def run_cmd(self, cmd, kwargs=None):
        try:
            rtn = ""
            out_msg = os.popen(cmd).readlines()
            for line in out_msg:
                rtn += line

            kwarg = {"cmd": str(cmd),
                     "work_type": "run_cmd",
                     "rtn": str(rtn),
                     }

            self.dbusDaemon.signal_kylin_root_run(SignalType.FINISH, kwarg)

        except Exception as e:
            print e
            kwarg = {"cmd": str(cmd),
                     "work_type": "run_cmd",
                     "rtn": str(e.message),
                     }

            self.dbusDaemon.signal_kylin_root_run(SignalType.ERROR, kwarg)

    # 执行 python 代码
    def run_python(self, pythons, kwargs=None):
        exec pythons

        kwarg = {"cmd": str(pythons),
                 "work_type": "run_python",
                 "rtn": "",
                 }

        self.dbusDaemon.signal_kylin_root_run(SignalType.FINISH, kwarg)


if __name__ == '__main__':
    cmd = "mkdir /1"
    out_msg = os.popen(cmd).readlines()