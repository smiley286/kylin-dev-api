#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
reload(sys)
sys.setdefaultencoding('utf8')

import dbus
import dbus.service
import dbus.mainloop.glib
import signal
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)
from dbus_daemon import *
from utils.enums import *


class DbusService:

    iface = None

    def __init__(self):
        self.init_dbus()

    def exit_dbus(self):
        self.iface.exit()

    def init_dbus(self):
        try:
            bus = dbus.SystemBus(mainloop)
        except:
            print("dbus init failed...")
            sys.exit(0)

        # dbus已经在运行，直接获取
        try:
            obj = bus.get_object(INTERFACE, "/")
            self.iface = dbus.Interface(obj, INTERFACE)
            self.iface.connect_to_signal("signal_kylin_root_run", self.slot_krr_signal)

        # dbus还未运行，启动一个新的
        except dbus.DBusException:
            os.environ["TERM"] = "xterm"
            os.environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/X11R6/bin"
            os.environ["DEBIAN_FRONTEND"] = "noninteractive"
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
            GObject.threads_init()
            signal.signal(signal.SIGINT, lambda : mainloop.quit())

            self.iface = Daemon(dbus.SystemBus(), mainloop)
            self.iface.connect_to_signal("signal_kylin_root_run", self.slot_krr_signal)
            mainloop.run()

    # root 执行命令行
    def call_root_run_cmd(self, cmd):
        self.iface.root_run_cmd(cmd)

    # root python 代码
    def call_root_run_python(self, pythons):
        self.iface.root_run_python(pythons)

    # kylin root run 后台传回的消息
    def slot_krr_signal(self, type, msg):
        signalType = type
        cmd = msg["cmd"]
        workType = msg["work_type"]
        rtn = msg["rtn"]

        print signalType, workType, cmd
        print rtn


if __name__ == "__main__":
    from PyQt4.QtCore import QCoreApplication
    app = QCoreApplication(sys.argv)
    d = DbusService()
    d.call_root_run_cmd("ls")

    sys.exit(app.exec_())
