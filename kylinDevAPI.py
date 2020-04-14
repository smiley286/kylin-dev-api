#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import signal
import dbus
import dbus.mainloop.glib
from gi.repository import GObject
from utils.single import SingleInstance
from dbus_daemon import Daemon

if __name__ == '__main__':
    myapp = SingleInstance("/tmp/kylinDevAPI-%d.pid" % os.getuid())
    if myapp.is_already_running():
       print "Another instance is running, exit."
       sys.exit("Another instance is running, exit.")

    os.environ["TERM"] = "xterm"
    os.environ["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/X11R6/bin"
    os.environ["DEBIAN_FRONTEND"] = "noninteractive"

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    GObject.threads_init()
    mainloop = GObject.MainLoop()
    signal.signal(signal.SIGINT, lambda : mainloop.quit())
    Daemon(dbus.SystemBus(), mainloop)
    mainloop.run()
