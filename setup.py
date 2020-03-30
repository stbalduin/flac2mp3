#!/usr/bin/env python
"""Setup file for flac2mp3 package"""
from os import path
from setuptools import setup, find_packages

with open('VERSION') as freader:
    VERSION = freader.readline().strip()
    
with open('README.md') as freader:
    README = freader.read()

with open('LICENSE') as freader:
    LICENSE = freader.read()
    
# Get required packages from requirements.txt
LOC = path.abspath(path.join(
    path.dirname(__file__), 'requirements.txt')
)
with open(LOC) as freader:
    REQUIREMENTS = freader.read().splitlines()
    

setup(
    name='flac2mp3',
    version=VERSION,
    description='A simple program to convert folders of .flac files'
                'to folders with .mp3 files.',
    author='Stephan Balduin <st.balduin@outlook.de>',
    author_email='st.balduin@outlook.de',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=REQUIREMENTS,
    # scripts=['bin/flac2mp3'],
    entry_points='''
        [console_scripts]
        flac2mp3=flac2mp3.cli:cli
    ''',
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python 3',
    ]
)
