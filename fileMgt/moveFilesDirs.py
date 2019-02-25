#!/usr/bin/env python

"""
Move files and subdirectories from a specified 'source' directory to a 'target' directory.
Any existing files & subdirectories in the 'target' directory but not in 'source' will remain intact.

example:

    ./moveFilesDirs.py -s ../source/ -t ../target/

This is based on my original answer to a Stack Overflow question:

    https://stackoverflow.com/revisions/7420617/1

"""

import os
import shutil
import argparse

# command line args
parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-s", "--source-filepath",
                    help="source directory to move", default=os.getcwd())
parser.add_argument("-t", "--target-filepath",
                    help="target directory to move to",
                    default=os.getcwd())
args = parser.parse_args()

# move files & directories
root_src_dir = args.source_filepath
root_dst_dir = args.target_filepath

for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.move(src_file, dst_dir)
