#!/usr/bin/env python

"""
backup a file to one or more target directories and create archived copies

example:

    ./backupFiles.py -s ../fileToBackup -t ../target/

notes:

    - removes older archived copies based on a specified minimum count (default of 3)
"""

import sys
sys.path.append('./common')
import filesUtil
import argparse
import os
import shutil
from datetime import datetime

# command line args
parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-s", "--source-filepath",
                    help="file to backup (copy)", default=os.getcwd())
parser.add_argument("-t", "--target-directories",
                    help="one or more target directories to backup (copy) file to",
                    default=os.getcwd(), nargs='+')
parser.add_argument("-c", "--archive-count",
                    help="minimum count of archived files (default of 3)", default="3")
args = parser.parse_args()

source_filepath = args.source_filepath
target_dirs = args.target_directories
min_archive_file_count = args.archive_count

# verify args
if not os.path.isfile(source_filepath):
    print("[ERROR] source file does not exist: {0}".format(source_filepath))
    sys.exit()

if min_archive_file_count.isdigit():
    min_archive_file_count = int(min_archive_file_count)
else:
    print("[ERROR] arg 'archive-count' is not an int: {0}".format(min_archive_file_count))
    sys.exit()
    
source_dir = os.path.dirname(source_filepath) 
root_filename = os.path.basename(source_filepath) 
archive_dirname = '_archive'
line_break = '\n' + '-' * 100

# check dirs & files exist
does_source_file_exist = filesUtil.dirs_exist([source_filepath])
do_any_target_dirs_exist = any([filesUtil.dirs_exist([dir_]) for dir_ in target_dirs])
if not all([does_source_file_exist, do_any_target_dirs_exist]):
    print("[ERROR] unable to backup file")
    sys.exit()

print("starting file backup...")
for target_dir in [dir_ for dir_ in target_dirs if os.path.exists(dir_)]:
    print(line_break * 2)
    print("target directory: {0}".format(target_dir))
    print(line_break * 2)

    # remove oldest archive backup file if more than minimum files count
    archive_dir = os.path.join(target_dir, archive_dirname)

    if not os.path.exists(archive_dir):
        print("creating archive directory: '{0}'...".format(archive_dir))
        os.makedirs(archive_dir)
        print("done!")

    archive_files = os.listdir(archive_dir)
    current_archive_file_count = len(archive_files)
    if current_archive_file_count > min_archive_file_count:
        archive_filename = min([file_ for file_ in archive_files if file_.startswith(root_filename)])
        archive_filepath = os.path.join(target_dir, archive_dir, archive_filename)
        os.remove(archive_filepath)
        print("minimum archive count: {0}".format(min_archive_file_count))
        print("current archive count: {0}\n".format(current_archive_file_count))
        print("one archive file removed:\n\t{0}".format(archive_filepath))
    else:
        print("current archive file count of {0} is below or at the minimum count of {1}\n"
              .format(current_archive_file_count, min_archive_file_count))
        print("0 archive files removed\n\t")

    # move current backup file to archive dir
    print(line_break)
    old_target_filepath = os.path.join(target_dir, root_filename)
    if os.path.exists(old_target_filepath):
        archive_timestamp = datetime.now().strftime('%Y%m%d')
        new_archive_filepath = os.path.join(target_dir, archive_dirname, root_filename + archive_timestamp)
        shutil.move(old_target_filepath, new_archive_filepath)
        print("moved the last previous backup file from\n\t{0}\nto\n\t{1}"
              .format(old_target_filepath, new_archive_filepath))
    else:
        print("[WARNING] old backup file\n\t{0}\ndoes not exist. unable to move to archive directory"
              .format(old_target_filepath))

    # copy latest file to backup dir
    print(line_break)
    if os.path.exists(source_filepath):
        shutil.copy2(source_filepath, target_dir)
        print("file '{0}' has been copied from\n\t{1}\nto\n\t{2}"
              .format(root_filename, os.path.abspath(source_dir), target_dir))
    else:
        print("[ERROR] source file\n\t{0} cannot be found".format(source_filepath))

print("done!")
