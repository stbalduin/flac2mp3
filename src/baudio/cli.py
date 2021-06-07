import os

import click

from . import LOG, util
from .core import gather_tasks, process_tasks


@click.command()
@click.argument(
    "src",
    type=click.Path(exists=True, dir_okay=True, readable=True, allow_dash=True),
)
@click.argument(
    "dst",
    type=click.Path(dir_okay=True, writable=True, allow_dash=True),
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    default=0,
    help="Set the verbosity level by repeating this option.",
)
@click.option(
    "--recursive",
    "-r",
    count=True,
    help="Recursively search for flac files and process them. "
    "Repeating this option increases the depth of the search.",
)
@click.option(
    "--copy-cover",
    "-c",
    "copy",
    is_flag=True,
    help="Copy the cover image to the new folder.",
)
@click.option("--no-act", "-n", "noact", is_flag=True, help="No action is done. ")
@click.option(
    "--bitrate",
    "-b",
    default="192k",
    help="Bitrate of the mp3s. Examples are 128k, 192k or 320k.",
)
@click.option(
    "--force", "-f", is_flag=True, help="Force conversion even if target file exists."
)
def baudio(src, dst, verbose, recursive, copy, noact, bitrate, force):
    # Setup logging
    util.setup_logging(verbose)

    # Input feedback
    LOG.debug("Initialized logging.")
    LOG.debug("Received the following inputs: ")
    LOG.debug("Source: %s", src)
    LOG.debug("Destination: %s", dst)
    LOG.debug("Recursive level: %s", recursive)
    LOG.debug("Copy cover: %s", copy)
    LOG.debug("Bitrate: %s", bitrate)
    LOG.debug("Force conversion: %s", force)
    LOG.debug("No action: %s", noact)

    # Recursion level
    recursive = max(0, min(5, recursive))
    LOG.info("Set recursiveness to %d", recursive)

    # Check the paths
    src_dir = util.get_dir(src)
    dst_dir = util.get_dir(dst)
    LOG.info("Source: %s.", src_dir)
    LOG.info("Destination: %s.", dst_dir)

    # If the last part of the path is different, the source root folder
    # is created at the destination. NOTE: This can be prevented if
    # the source root folder ends with / while the destination
    # folder ends with something different (or if both end with /)
    src_path = os.path.split(src_dir)
    dst_path = os.path.split(dst_dir)
    if src_dir == dst_dir:
        dst_dir = os.path.join(dst_dir, "mp3")
    if src_path[-1] != dst_path[-1]:
        dst_dir = os.path.join(dst_dir, src_path[-1])

    # Do the work part 1
    tasks = gather_tasks(
        src_dir, dst_dir, max_depth=recursive, copy_cover=copy, bitrate=bitrate
    )

    # Do the work part 2
    if noact:
        LOG.warning("No action performed. This would be the result: ")
        util.list_tasks(tasks)
    else:
        process_tasks(tasks)
