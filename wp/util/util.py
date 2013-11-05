"""@package wp.util
Common utilities for the wp module
"""

import os
import shutil
import errno
import glob

def mkdir_p(path):
    """implements `mkdir -p`."""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def get_wp_dir():
    """returns the system's wallpaper directory.
    Default `~/.wallpapers`, or $WALLPAPERS_DIR if set"""
    wallpapers_dir=os.getenv('WALLPAPERS_DIR', os.environ['HOME']+'/.wallpapers')
    try:
        mkdir_p(wallpapers_dir)
        return wallpapers_dir
    except:
        raise

def get_wp_files():
    """returns a list of images located in the wallpaper directory."""
    wp_dir=get_wp_dir()
    types=('*.jpg','*.jpeg','*.png')
    files=[]
    for t in types:
        files.extend(glob.glob(wp_dir+'/'+t))
    return files