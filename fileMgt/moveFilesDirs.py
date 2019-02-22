"""
Move files and subdirectories from a specified 'source' directory to a 'destination' directory.
Any existing files & subdirectories in the 'destination' directory but not 'source' will not be removed.

This is based on my original answer to a Stack Overflow question:

    https://stackoverflow.com/revisions/7420617/1

"""

import os
import shutil

root_src_dir = 'Src Directory\\'
root_dst_dir = 'Dst Directory\\'

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
