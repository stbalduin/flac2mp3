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
@click.option(
    '--bitrate', '-b', default='192k',
    help='Bitrate of the mp3s. Examples are 128k, 192k or 320k.'
)
def cli(src, dst, recursive, verbose, copy, noact, bitrate):
    
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
    log.trace('Bitrate: {}'.format(bitrate))
    
    # Recursion level
    recursive = max(0, min(4, recursive))  # Could be higher, though
    log.debug('Setting recursiveness to {}.'.format(recursive))

    # Check the paths
    src_dir = util.get_dir(src)
    dst_dir = util.get_dir(dst)
    
    # If the last part of the path is different, the source root folder
    # is created at the destination. NOTE: This can be prevented if
    # the source root folder ends with / while the destination
    # folder ends with something different (or if both end with /)
    src_path = path.split(src_dir)
    dst_path = path.split(dst_dir)
    if src_dir == dst_dir:
        dst_dir = path.join(dst_dir, 'mp3')
    if src_path[-1] != dst_path[-1]:
        dst_dir = path.join(dst_dir, src_path[-1])

    # Do the work part 1
    tasks = gather_tasks(src_dir, dst_dir, 
                         max_depth=recursive, 
                         copy_cover=copy,
                         bitrate=bitrate)

    # Do the work part 2
    if noact:
        log.warn('No action performed. This would be the result: ')
        util.list_tasks(tasks)
    else:
        process_tasks(tasks)


if __name__ == '__main__':
    cli()
