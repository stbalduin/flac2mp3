import os
from os import path

import click

from flac2mp3 import log


def get_dir(target):
    log.trace('Checking directory {}'.format(target))

    if target.startswith('/'):
        log.trace('"{}" is an absolute path'.format(target))
    else:
        log.trace('"{}" is a relative path'.format(target))
        target = path.abspath(path.join(os.getcwd(), target))

    return target


def list_tasks(tasks):
    for task in tasks:
        if task[0] == 'mkdir':
            click.echo('[Create directory] {}.'.format(task[1]))
        elif task[0] == 'copy':
            click.echo('[Copy] {} --> {}'.format(task[1], task[2]))
        elif task[0] == 'convert':
            click.echo('[Convert] {} --> {}'.format(task[1], task[2]))
