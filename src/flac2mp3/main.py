#!/usr/bin/env python
import os
from shutil import copy2
from pydub import AudioSegment
from pydub.utils import mediainfo
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error


def process_folder(src_dir, dst_dir):
    files = os.listdir(src_dir)
    cover = 'folder.jpeg'
    if not os.path.isfile(os.path.join(src_dir, cover)):
        cover = 'folder.jpg'
    if not os.path.isfile(os.path.join(src_dir, cover)):
        cover = 'folder.png'
    if not os.path.isfile(os.path.join(src_dir, cover)):
        cover = 'cover.png'
    if not os.path.isfile(os.path.join(src_dir, cover)):
        cover = 'cover.jpg'
    src_cover = os.path.join(src_dir, cover)
    dst_cover = os.path.join(dst_dir, cover)

    if os.path.isfile(src_cover):
        copy2(src_cover, dst_cover)
    else:
        print('No folder.jpeg found in "%s"' % src_dir)
        dst_cover = None 

    for audio_file in files:
        if audio_file.endswith('.flac'):
            audio_type = 'flac'
        elif audio_file.endswith('wma'):
            audio_type = 'wma'
        elif audio_file.endswith('flv'):
            audio_type = 'flv'
        else:
            # Not an audio file
            continue
        print('Processing file "%s" ... ' % audio_file, end='')
        process_file(src_dir, dst_dir, audio_file, dst_cover, audio_type)
        print('Done!')

def process_file(src_dir, dst_dir, filename, dst_cover, audio_type):
    src_file = os.path.join(src_dir, filename)
    dst_file = filename[:-5] + '.mp3'
    dst_file = os.path.join(dst_dir, dst_file)
    if os.path.isfile(dst_file):
        return False
    print(audio_type)
    flac_audio = AudioSegment.from_file(src_file, format=audio_type)
    meta = mediainfo(src_file).get('TAG', {})
    flac_audio.export(dst_file, format='mp3', bitrate='196k', tags=meta)

    if dst_cover is None:
        return False

    mp3_audio = MP3(dst_file, ID3=ID3)
    try:
        mp3_audio.add_tags()
    except error:
        pass

    with open(dst_cover, 'rb') as img:
        cover = img.read()
    
    mime = 'image/jpeg'
    if dst_cover.endswith('.png'):
        mime = 'image/png'

    mp3_audio.tags.add(APIC(
        encoding=3,  # utf-8
        mime=mime,  # image/png or image/jpeg
        type=3,  # front cover
        data=cover
    ))
    mp3_audio.save()
    return True



def main():
    # Create the output root directory
    dst_root = os.path.join('..', '..', 'mp3')
    if not os.path.isdir(dst_root):
        os.makedirs(dst_root)
    
    # Read the source directories
    src_dirs = os.listdir()
    cwd = os.getcwd()
    print('Found %d items in dir %s:' % (len(src_dirs), cwd))
    print(src_dirs)
    non_dirs = 0
    for src_dir in src_dirs:
        if not os.path.isdir(src_dir):
            # It is a file and not a directory
            non_dirs += 1
            continue
        # Create current output directory
        dst_dir = os.path.join(dst_root, src_dir)
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        
        print('Processing directory [%s] ---> [%s] ...' % (src_dir, dst_dir))
        process_folder(src_dir, dst_dir)
    if non_dirs > 0:
        dst_dir = os.path.abspath(
            os.path.join(dst_root, os.path.split(cwd)[-1])
        )
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        print('Processing directory [%s] ---> [%s] ...' % (cwd, dst_dir))
        process_folder(cwd, dst_dir)


if __name__ == '__main__':
    main()
