# import wp modules
from wp.cluster import *
from wp.model import *
from wp.io import *
from wp.gui import *

# import deps
import os
import shutil
import errno
import glob

# Version string.  Imported by setup.py :)
__version__="0.1.0"

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def get_wp_dir():
    wallpapers_dir=os.getenv('WALLPAPERS_DIR', os.environ['HOME']+'/.wallpapers')
    try:
        mkdir_p(wallpapers_dir)
        return wallpapers_dir
    except:
        raise

def get_wp_files():
    wp_dir=get_wp_dir()
    types=('*.jpg','*.jpeg','*.png')
    files=[]
    for t in types:
        files.extend(glob.glob(wp_dir+'/'+t))
    return files

###############################################################################
# ADD image files to your wallpaper directory and processes colors
# TODO check for file input type
# TODO compute color scheme :)
def add(args):
    wp_dir=get_wp_dir()
    for f in args.arg:
        f_base=os.path.basename(f)
        f_dst=wp_dir+'/'+f_base
        shutil.copy(f,f_dst)

###############################################################################
# CHANGE current background.  If no args provided, choose a random wallpaper
def change(args):
    print args # placeholder

###############################################################################
# LIST all wallpapers in collection
def list(args):
    files=get_wp_files()

    if(args.a):
        print '\n'.join(files)
    else:
        print '\n'.join([os.path.basename(f) for f in files])

###############################################################################
# REMOVE a wallpaper from your collection
# TODO autocomplete?
def remove(args):
    for a in args.arg:
        files=get_wp_files()
        for f in files:
            if os.path.basename(f) == a:
                os.remove(os.path.abspath(f))
                # color files for <img> are /.<img>.<format>
                for c in glob.glob(get_wp_dir()+'/.'+a+'*'): 
                    os.remove(os.path.abspath(c))
                break
