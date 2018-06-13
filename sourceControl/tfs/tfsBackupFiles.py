"""
backup files with tfs pending changes
"""

import sys
import os
import shutil
import subprocess
import errno
from time import gmtime, strftime
import argparse

# command line args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-t", "--tfs-branch-dir", help="directory of tfs branch", default=os.getcwd())
parser.add_argument("-b", "--backup-dir", help="backup directory to copy files with pending changes", default=os.getcwd())
args = parser.parse_args()

tfs_branch_dir = args.tfs_branch_dir
root_backup_dir = args.backup_dir

# verify directories
if tfs_branch_dir == root_backup_dir:
    print('unable to copy files. tfs branch and backup directories are the same')
    sys.exit()

# create backup directory
bkup_timestamp = strftime("%Y-%m-%d_%H_%M_%S", gmtime())
backup_dir = os.path.join(root_backup_dir, bkup_timestamp)

if not os.path.exists(backup_dir):
    print("creating backup directory: '{0}'...".format(backup_dir))
    os.makedirs(backup_dir)
    print("done!")

# get filepath names from tfs status
tfs_status_command = r'tf status {0} /r'.format(tfs_branch_dir)
output = subprocess.check_output(tfs_status_command, shell=True)
drive_letter = os.path.splitdrive(tfs_branch_dir)[0]
files = [line[line.index(drive_letter):].strip()
         for line in output.splitlines()
         if len(line) != 0 and drive_letter in line]

# copy pending files to backup directory
def printTargetDir():
    print("current files in backup directory: '{0}'...".format(backup_dir))
    files_ = os.listdir(backup_dir)
    if len(files_) > 0:
        for file_ in os.listdir(backup_dir):
            print("\t{0}".format(file_))
    else:
        print("no files found!")

print('')
printTargetDir()
print('-' * 100)
print('copying files with tfs pending changes...')
for file_ in files:

    print("\t{0}".format(file_))

    if not os.path.isfile(file_):
        print("file does not exist: {0}".format(file_))
        continue

    shutil.copy2(file_, backup_dir)

print('done!')
print('-' * 100)
printTargetDir()

