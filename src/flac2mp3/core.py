"""This is the core module."""

from os import listdir, path
from shutil import copy2

from mutagen.id3 import APIC, ID3, error
from mutagen.mp3 import MP3
from pydub import AudioSegment
from pydub.utils import mediainfo

from flac2mp3 import log


def gather_tasks(src_dir, 
                 dst_dir, 
                 max_depth=1, 
                 copy_cover=True, 
                 depth=0):
    tasks = list()
    
    log.trace('Gathering tasks in {}'.format(src_dir))

    if not path.exists(src_dir):
        log.error('Source path "{}" does not exist'.format(src_dir))
        return tasks
    if not path.exists(dst_dir):
        tasks.append(['mkdir', dst_dir])    

    cover = _collect_cover(src_dir)
    cover_src = None
    if cover is not None:
        cover_src = path.join(src_dir, cover)
        cover_dst = path.join(dst_dir, cover)
        if copy_cover:
            tasks.append(['copy', cover_src, cover_dst])
        log.trace('Found a cover with the name: "{}"'.format(cover_src))
    else:
        log.info('No cover found. Make sure to have a "folder.jpg" '
                 'if you want to keep the album cover')

    files = _collect_files(src_dir)
    if len(files) == 0:
        log.info('No .flac files found in the current directory.')

    for flac in files:
        flac_src = path.join(src_dir, flac)
        mp3_dst = path.join(src_dir, '{}.mp3'.format(flac[:-5]))
        tasks.append(['convert', flac_src, mp3_dst, cover_src])

    if depth < max_depth:
        dirs = _collect_dirs(src_dir)
        log.trace('Found subdirectories '
                  '(Recursivity {}/{})'.format(depth, max_depth))
        for sub_dir in dirs:
            sub_src = path.join(src_dir, sub_dir)
            sub_dst = path.join(dst_dir, sub_dir)
            sub_tasks = gather_tasks(sub_src, sub_dst, 
                                     max_depth=max_depth, 
                                     depth=depth+1,
                                     copy_cover=copy_cover)
            tasks.append([
                'subfolder', sub_src, sub_dst, sub_tasks
            ])
    else:
        log.debug('Maximal recursion level {} reached.'.format(max_depth))
    
    return tasks


def _collect_files(src_dir):
    files = list()
    for item in listdir(src_dir):
        if path.isfile(path.join(src_dir, item)):
            if item.lower().endswith('.flac'):
                files.append(item)

    return files


def _collect_dirs(src_dir):
    return [item for item in listdir(src_dir) 
            if path.isdir(path.join(src_dir, item))]


def _collect_cover(src_dir):
    """Look for an album cover image.

    TODO: look for files in the directory and compare it to
    one of the names instead the other way round.

    """
    cover_names = ['folder', 'cover', 'FOLDER', 'COVER']
    cover_types = ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG']

    files = listdir(src_dir)

    for cname in cover_names:
        for ctype in cover_types:
            cover = '{}.{}'.format(cname, ctype)
            if path.isfile(path.join(src_dir, cover)):
                return cover
     
    return None


def process_tasks(tasks):
    if len(tasks) == 0:
        log.error('Nothing to do.')
        return
        
