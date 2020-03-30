"""This module provides very simple logging functionality.""" 
import click

VERBOSITY = 0
LVLS = {
    0: 'ERROR',
    1: ' WARN',
    2: ' INFO',
    3: 'DEBUG',
    4: 'TRACE'
}


def _log(msg, lvl=3, set_verbosity=None):
    """Logs a message to console.

    The content of *msg* will be printed to console using clicks echo
    function. The value of *lvl* will be compared with the global
    verbosity level which can be altered with *set_verbosity'. A higher
    value of *lvl* requires higher verbosity level to be printed.
    
    """
    global VERBOSITY
    if set_verbosity is not None:
        VERBOSITY = set_verbosity

    if lvl <= VERBOSITY:
        click.echo('[flac2mp3][{}] {}'.format(LVLS[lvl], msg))

def error(msg):
    _log(msg, 0)

def warn(msg):
    _log(msg, 1)

def info(msg):
    _log(msg, 2)

def debug(msg):
    _log(msg, 3)

def trace(msg):
    _log(msg, 4)