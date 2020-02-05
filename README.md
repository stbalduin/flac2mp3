# flac2mp3
A simple program to convert folders of .flac files to folders with .mp3 files.  

## Install
Clone the repository and change into the root directory of the repository. 
If you want to use the program directly from your shell, execute

```bash
sudo python setup.py install
```

Otherwise, optionally create a virtualenv and install via pip.

```bash
pip install .
```
## Usage

Change into the directory where the .flac files are. If installed as system-wide shell script, execute

```bash
flac2mp3
```
If installed via pip, execute

```bash
python -m flac2mp3.flac2mp3 
```
