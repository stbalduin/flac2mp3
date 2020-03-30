import os
from os import path

import click

from flac2mp3 import log, util
from flac2mp3.core import gather_tasks, process_tasks


@click.command()
@click.option(
    '--src', '-i', default='.', 
    help='Path to the folder where the source files are located.'
)
@click.option(
    '--dst', '-o', default='.',
    help='Path to the folder where the converted files will be saved.'
)
@click.option(
    '--recursive', '-r', count=True,
    help='Recursively search for flac files and process them. '
         'Repeating this option increases the depth of the search.'
)
@click.option(
    '--verbose', '-v', count=True,
    help='Set the verbosity level by repeating this option.'
)
@click.option(
    '--copy-cover', '-c', 'copy', is_flag=True,
    help='Copy the cover image to the new folder.'
)
@click.option(
    '--no-act', '-n', 'noact', is_flag=True,
    help='No action is done. '
)
def cli(src, dst, recursive, verbose, copy, noact):
    
    # Setup logging
    loglvl = max(0, min(4, verbose))
    log._log('Setting verbosity to {}.'.format(loglvl), 3, loglvl)

    # Input feedback
    log.trace('Got the following inputs:')
    log.trace('Source: {}'.format(src))
    log.trace('Destination: {}'.format(dst))
    log.trace('Recursive lvl: {}'.format(recursive))
    log.trace('Verbosity: {}'.format(verbose))
    log.trace('Copy cover: {}'.format(copy))
    log.trace('No action: {}'.format(noact))
    
    # Recursion level
    recursive = max(0, min(4, recursive))  # Could be higher, though
    log.debug('Setting recursiveness to {}.'.format(recursive))

    # Check the paths
    src_dir = util.get_dir(src)
    dst_dir = util.get_dir(dst)
    
    # Do the work part 1
    tasks = gather_tasks(src_dir, dst_dir, 
                         max_depth=recursive, 
                         copy_cover=copy)

    # Do the work part 2
    if noact:
        util.list_tasks(tasks)
    else:
        process_tasks(tasks)


if __name__ == '__main__':
    cli()
