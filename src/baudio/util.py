import logging
import os
from os import path

import click

from . import LOG


def get_dir(target):
    LOG.info("Checking directory {}".format(target))

    if target.startswith("/"):
        LOG.debug('"{}" is an absolute path'.format(target))
    else:
        LOG.debug('"{}" is a relative path'.format(target))
        target = path.abspath(path.join(os.getcwd(), target))

    return target


def list_tasks(tasks):
    for task in tasks:
        if task[0] == "mkdir":
            click.echo("[Create directory] {}.".format(task[1]))
        elif task[0] == "copy":
            click.echo("[Copy] {} --> {}".format(task[1], task[2]))
        elif task[0] == "convert":
            click.echo("[Convert] {} --> {}".format(task[1], task[2]))


def setup_logging(verbose):
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = levels[verbose if verbose < len(levels) else len(levels) - 1]

    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )

    logging.getLogger("pydub").setLevel(logging.WARNING)