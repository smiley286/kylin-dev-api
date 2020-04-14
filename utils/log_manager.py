#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "huangsheng"

import os, sys
reload(sys)
sys.setdefaultencoding('utf8')
import logging, logging.handlers


class LogManager():
    LOG = None

    @classmethod
    def INFO(self, msg):
        return self.LOG.info(msg)

    @classmethod
    def WARN(self, msg):
        return self.LOG.warning(msg)

    @classmethod
    def ERR(self, msg):
        return self.LOG.error(msg)

    @classmethod
    def CRI(self, msg):
        return self.LOG.critical(msg)


def init_log():
    cache_dir = os.environ.get('XDG_CACHE_HOME','').strip()
    if not cache_dir:
        cache_dir = os.path.expanduser("~/.cache")
    log_file = os.path.join(cache_dir, "krr.log")
    LogManager.LOG = logging.getLogger("KRR")
    LogManager.LOG.propagate = False
    LogManager.LOG.setLevel(logging.DEBUG)
    log_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    log_formatter = logging.Formatter("[%(asctime)s - %(levelname)s - %(message)s")
    log_handler.setFormatter(log_formatter)
    LogManager.LOG.addHandler(log_handler)

