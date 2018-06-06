#!/usr/bin/env python

"""
export radio files generated by sandisk sansa fuze

example:

    ./export_radio_files.py -s ../source/ -t ../target/

notes:

- also removes the files from the sansa fuze device (i.e. "source" directory)
- files should be WAV format specifically with the following file name pattern used by sansa fuze:

    <radio station call sign>_MMDDYY_<version count>.wav

    for example:

        88-1_121811_001.wav

- removes oldest target directory files matching above file pattern and keeping oldest three

"""

import os
from time import mktime
import sys
sys.path.append('./common')
import files_util
import argparse

# command line args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-s", "--source-directory", help="source directory containing radio files to move", default=os.getcwd())
parser.add_argument("-t", "--target-directory", help="target directory to move radio files to", default=os.getcwd())
args = parser.parse_args()

source_dir = args.source_directory
target_dir = args.target_directory
FILE_EXT = 'wav'

# verify dirs
if source_dir == target_dir:
    print('Unable to move files. Source and target directories are the same')
    sys.exit()

if not files_util.dirs_exist([source_dir, target_dir]):
    print('Unable to move files. Source and/or target directories do not exist.')
    sys.exit()

# remove old files from target directory
print('Removing oldest files from target directory...')

old_files = os.listdir(target_dir)
old_file_count = len([file_ for file_ in old_files if file_.lower().endswith('001.' + FILE_EXT)])

if old_file_count >= 3:
    get_time = lambda file_ : mktime((0, 0, 0, int(file_[5:7]), int(file_[7:9]), int(file_[9:11]), 0, 0, 0))
    file_times = [(file_, get_time(file_)) for file_ in old_files if file_.endswith('.' + FILE_EXT.upper())]
    oldest_time = min([time_ for file_, time_ in file_times])

    def remove_file(file_):
        try:
            os.remove(os.path.join(target_dir, file_))
            print('The file ' + file_ + ' has been removed.')
        except OSError as e:
            print("Unable to remove oldest files from target directory\n" + e)

    [remove_file(file_) for file_, time_ in file_times if time_ == oldest_time]
else:  
    print("Skipping removing oldest files since only {0} file(s) exist.  Must have at least three (3) files before removing any old files.".format(old_file_count))

# move new files to target directory

files_util.move_files(source_dir, target_dir, FILE_EXT, "radio")