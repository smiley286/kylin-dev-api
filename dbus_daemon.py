#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import dbus.service
import dbus.mainloop.glib
import time
import threading
from dbus_worker import Worker
from utils.enums import *

import subprocess


class WorkItem:
     def __init__(self, cmd, workType, kwargs):
        self.cmd = cmd
        self.workType = workType
        self.kwargs = kwargs

class WorkThread(threading.Thread):

    def __init__(self, dbusDaemon):
        threading.Thread.__init__(self)
        self.dbusDaemon = dbusDaemon
        print "KylinRootRun dbus start", type(self.dbusDaemon)

    def run(self):
        while(True):

            if len(self.dbusDaemon.workList) == 0:
                time.sleep(0.2)
                continue

            self.dbusDaemon.mutex.acquire()
            item = self.dbusDaemon.workList.pop(0)
            self.dbusDaemon.mutex.release()

            func = getattr(self.dbusDaemon.worker, item.workType)

            if func is None:
                print "Error workType: ", item

            res = func(item.cmd, item.kwargs)

            if res is False:
                print "work exec failed: ", item.cmd

            time.sleep(0.2)


class Daemon(dbus.service.Object):

    def __init__ (self, bus, mainloop):
        self.bus = bus
        self.bus_name = dbus.service.BusName("cn.kylinos.KylinDevAPI", bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, "/")
        self.mainloop = mainloop

        self.worker = Worker(self)

        self.workList = []
        self.mutex = threading.RLock()
        self.worker_thread = WorkThread(self)
        self.worker_thread.setDaemon(True)
        self.worker_thread.start()

    def stop(self):
        # 停止本程序dbus，并从系统bus中移除
        self.remove_from_connection()

    def add_worker_item(self, item):
        self.mutex.acquire()
        self.workList.append(item)
        self.mutex.release()

    @dbus.service.method(INTERFACE, in_signature='', out_signature='')
    def exit(self):
        self.mainloop.quit()

    # 执行本地命令
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='b', sender_keyword='sender')
    def root_run_cmd(self, cmd, sender=None):
        print "run command: ", cmd

        item = WorkItem(cmd, WorkType.RUNCMD, None)

        self.add_worker_item(item)

        return True

    # 执行 python 代码
    @dbus.service.method(INTERFACE, in_signature='as', out_signature='b', sender_keyword='sender')
    def root_run_python(self, pythons, sender=None):
        print "run python code: ", pythons

        item = WorkItem(pythons, WorkType.RUNPYTHON, None)

        self.add_worker_item(item)

        return True

    # 修改 密码
    @dbus.service.method(INTERFACE, in_signature='ss', out_signature='b', sender_keyword='sender')
    def changePwd(self, userName, newPasswd, sender=None)
        cmd = []
        cmd.append("passwd")
        cmd.append(userName)
        p = subprocess.Popen(cmd, env={'LANGUAGE':'en:'}, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        p.stdin.write(newPasswd)
        p.stdin.write("\n")
        p.stdin.write(newPasswd)
        p.stdin.write("\n")

    # 测试函数
    @dbus.service.method(INTERFACE, in_signature='i', out_signature='i')
    def test_return_value(self, arg):
        return 2 + arg

    # 交互信号
    '''parm mean
        type:
            FINISH: work finished
            ERROR = work error
        msg:
            kwargs{...}
    '''
    @dbus.service.signal(INTERFACE, signature='sa{ss}')
    def signal_kylin_root_run(self, type, msg):
        pass
