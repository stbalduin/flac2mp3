#!/usr/bin/env python
"""Setup file for flac2mp3 package"""
from os import path

import setuptools

with open("VERSION") as freader:
    VERSION = freader.readline().strip()

with open("README.md") as freader:
    README = freader.read()

# Get required packages from requirements.txt
LOC = path.abspath(path.join(path.dirname(__file__), "requirements.txt"))
with open(LOC) as freader:
    REQUIREMENTS = freader.read().splitlines()

install_requirements = [
    "click",
    "mutagen",
    "pydub",
]
development_requirements = [
    "black",
    "flake8",
    # "pytest"
]

extras = {"dev": development_requirements}

setuptools.setup(
    name="baudio",
    version=VERSION,
    author="Stephan Balduin <st.balduin@outlook.de>",
    author_email="st.balduin@outlook.de",
    description="A simple program to convert folders of .flac files"
    "to folders with .mp3 files.",
    long_description=README,
    long_description_content_type="test/markdown",
    url="https://gitlab.com/stbalduin/baudio",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=install_requirements,
    extras_require=extras,
    entry_points="""
        [console_scripts]
        baudio=baudio.cli:baudio
    """,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python 3",
    ],
)
