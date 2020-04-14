#!/usr/bin/env python

import glob
from distutils.core import setup

data_files=[
        ('../etc/dbus-1/system.d/',['conf/cn.kylinos.KylinDevAPI.conf']),
        ('share/dbus-1/system-services/',['conf/cn.kylinos.KylinDevAPI.service']),
        ('share/kylin-dev-api/', ['kylinDevAPI.py']),
        ('share/kylin-dev-api/', ['caller_demo.py']),
        ('share/kylin-dev-api/', ['dbus_daemon.py']),
        ('share/kylin-dev-api/', ['dbus_worker.py']),
        ('share/kylin-dev-api/utils/', glob.glob('utils/*')),
        ]

setup(name="kylin-dev-api",
      version="1.0.0",
      author="Kylin Development Team",
      author_email="zdcp@kylinos.cn",
      url="www.kylinos.cn",
      license="GNU General Public License (GPL)",
      data_files=data_files,
      )
