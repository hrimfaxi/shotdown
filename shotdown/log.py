#!/usr/bin/python2
# coding: utf-8

import logging
from logging import DEBUG, INFO, WARNING, ERROR

_logger = debug = info = warning = error = setlevel = None

def init_logger(loglevel):
    global _logger, debug, info, warning, error, setlevel
    _logger = logging.getLogger('shotdown')

    level = logging.DEBUG
    if loglevel == 'debug':
        level = logging.DEBUG
    elif loglevel == 'error':
        level = logging.ERROR
    elif loglevel == 'warning':
        level = logging.WARNING
    elif loglevel == 'info':
        level = logging.INFO

    _logger.setLevel(level)
    _logger.handlers = []
    handler = logging.StreamHandler()
    FORMAT = logging.Formatter('%(asctime)-15s %(levelname)s: %(message)s')
    handler.setFormatter(FORMAT)
    _logger.addHandler(handler)

    debug = _logger.debug
    info = _logger.info
    warning = _logger.warning
    error = _logger.error
    setlevel = _logger.setLevel

# vim: set tabstop=4 sw=4 expandtab:
