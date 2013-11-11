#! /usr/bin/env python

import sys, os
from distutils.core import setup
import wp 

long_description=open('README.md').read()

setup_args = dict(
    name='wp',
    version=wp.__version__,
    description='Wallpaper Manager',
    author='Caleb Everett',
    url='http://github.com/The-Apiary/wp',
    packages=['wp','wp.palette'],
    scripts=['scripts/wp'],
 )

if __name__ == '__main__':
    setup(**setup_args)
