#!/usr/bin/python
# -*- coding: utf-8 -*-

import gettext
gettext.textdomain("kylin-dev-api")
_ = gettext.gettext

VERSION = "v1.0.-"

INTERFACE = "cn.kylinos.KylinDevAPI"
INTERFACES = "/cn/kylinos/KylinDevAPI"

class WorkType:
    RUNCMD = "run_cmd"
    RUNPYTHON = "run_python"

class SignalType:
    FINISH = "root_run_finish"
    ERROR = "root_run_error"
