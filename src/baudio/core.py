"""This is the core module."""

from os import listdir, makedirs, path
from shutil import copy2

import click
from mutagen.id3 import APIC, ID3, error
from mutagen.mp3 import MP3
from pydub import AudioSegment
from pydub.utils import mediainfo

from . import LOG


def gather_tasks(
    src_dir, dst_dir, bitrate, max_depth=1, copy_cover=True, depth=0, force=False
):

    LOG.info("Gathering tasks in %s.", src_dir)
    LOG.debug("Recursivity: %d/%d", depth, max_depth)

    tasks = list()

    # Check paths (again)
    if not path.exists(src_dir):
        LOG.error('Source path "%s" does not exist', src_dir)
        return tasks

    if not path.exists(dst_dir):
        tasks.append(["mkdir", dst_dir])

    # Look for cover
    cover = _collect_cover(src_dir)
    cover_src = None
    if cover is not None:
        cover_src = path.join(src_dir, cover)
        cover_dst = path.join(dst_dir, cover)
        if copy_cover:
            tasks.append(["copy", cover_src, cover_dst])
        LOG.debug('Found a cover with the name: "%s"', cover_src)
    else:
        LOG.warning(
            "No cover found in the current directory. Make sure "
            'to have a "folder.jpg" if you want to keep the album '
            "cover."
        )

    # Search for files to process
    files = _collect_files(src_dir)
    if len(files) == 0:
        LOG.info("No .flac files found in the current directory.")

    for flac in sorted(files):
        flac_src = path.join(src_dir, flac)
        mp3_dst = path.join(dst_dir, "{}.mp3".format(flac[:-5]))
        if not path.isfile(mp3_dst) or force:
            tasks.append(["convert", flac_src, mp3_dst, cover_src, "flac", bitrate])
        else:
            LOG.debug("Destination file %s already exists. Skipping this one.", mp3_dst)
    # Search for sub directories to process
    if depth < max_depth:
        dirs = _collect_dirs(src_dir)
        for sub_dir in sorted(dirs):
            sub_src = path.join(src_dir, sub_dir)
            sub_dst = path.join(dst_dir, sub_dir)
            sub_tasks = gather_tasks(
                sub_src,
                sub_dst,
                max_depth=max_depth,
                depth=depth + 1,
                copy_cover=copy_cover,
                bitrate=bitrate,
            )
            for task in sub_tasks:
                tasks.append(task)
    else:
        LOG.debug("Maximal recursion level %s reached.", max_depth)

    return tasks


def _collect_files(src_dir):
    files = list()
    for item in listdir(src_dir):
        if path.isfile(path.join(src_dir, item)):
            if item.lower().endswith(".flac"):
                files.append(item)

    return files


def _collect_dirs(src_dir):
    return [item for item in listdir(src_dir) if path.isdir(path.join(src_dir, item))]


def _collect_cover(src_dir):
    """Look for an album cover image.

    TODO: look for files in the directory and compare it to
    one of the names instead the other way round.

    """
    cover_names = ["folder", "cover", "FOLDER", "COVER"]
    cover_types = ["jpg", "jpeg", "png", "JPG", "JPEG", "PNG"]

    files = listdir(src_dir)

    for cname in cover_names:
        for ctype in cover_types:
            cover = f"{cname}.{ctype}"
            if path.isfile(path.join(src_dir, cover)):
                return cover

    return None


def process_tasks(tasks):
    num_tasks = len(tasks)
    if num_tasks == 0:
        LOG.warning("Nothing to do.")
        return

    LOG.info("Start processing %d tasks.", num_tasks)
    with click.progressbar(length=num_tasks, label="Converting files") as bar:
        for task in tasks:
            if task[0] == "mkdir":
                LOG.info("Creating directory %s.", task[1])
                makedirs(task[1])
            elif task[0] == "copy":
                LOG.info("Copying file %s to %s.", task[1], task[2])
                copy2(task[1], task[2])
            elif task[0] == "convert":
                LOG.info("Converting file %s to %s.", task[1], task[2])
                _process_file(task[1], task[2], task[3], task[4], task[5])
            else:
                LOG.error("Invalid command {}.".format(task[0]))
            bar.update(1)


def _process_file(src, dst, cover_path, audio_type_src, bitrate, audio_type_dst="mp3"):

    LOG.debug("Reading source file: %s.", src)
    src_file = AudioSegment.from_file(src, format=audio_type_src)

    LOG.debug("Reading tags from file")
    meta = mediainfo(src).get("TAG", {})

    LOG.debug("Creating destination file: %s.", dst)
    src_file.export(dst, format=audio_type_dst, bitrate=bitrate, tags=meta)

    LOG.debug("Reading cover file: %s.", cover_path)

    # TODO: Check if the cover parameter of export also works.
    if cover_path is None:
        LOG.info("No cover to add.")
        # No cover, therefore we're finished with this file
        return False

    # Prepare the cover
    with open(cover_path, "rb") as img:
        cover = img.read()

    mime = "image/jpeg"
    if cover_path.endswith(".png"):
        mime = "image/png"

    LOG.debug("Reading destination file.")
    if audio_type_dst == "mp3":
        dst_file = MP3(dst, ID3=ID3)
        try:
            dst_file.add_tags()
        except:
            # Tag already exists
            pass
    else:
        LOG.warning("Only .mp3 are supported as output format.")
        return False

    LOG.debug("Adding cover to destination file.")
    dst_file.tags.add(
        APIC(
            encoding=3,  # utf-8
            mime=mime,  # image/png or image/jpeg
            type=3,  # front cover
            data=cover,  # the image
        )
    )

    LOG.debug("Saving info in destination file.")
    dst_file.save()

    return True
