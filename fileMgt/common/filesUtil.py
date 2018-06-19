""" file management utilities

funcs to bulk copy/move files, etc.

"""

import os
import shutil

def move_files(source_dir, target_dir, file_ext, file_description):
    """ move files from one directory to another """

    def move_file(file_):
        try:
            print("Moving file '{0}'...".format(file_))
            shutil.move(os.path.join(source_dir, file_), target_dir)
            print("Done!")
        except OSError as e:
            print("Unable to move file '" + file_ )
            print e.errno
            print e.filename
            print e.strerror

    files = [file_ for file_ in os.listdir(source_dir) if file_.lower().endswith(file_ext.lower())]

    print("\nMoving '{2}' file(s) from\n\t{0}\nto\n\t{1}\nstarting...".format(source_dir, target_dir, file_description))
    [move_file(file_) for file_ in files]
    print('\nAll done! {0} file(s) have been moved.\n'.format(str(len(files))))

def copy_files(source_dir, target_dir, file_ext, file_description):
    """ copy files from one directory to another """

    def copy_file(file_):
        try:
            print("Copying file '{0}'...".format(file_))
            shutil.copy(os.path.join(source_dir, file_), target_dir)
            print("Done!")
        except OSError as e:
            print("Unable to copy file '" + file_ )
            print e.errno
            print e.filename
            print e.strerror

    files = [file_ for file_ in os.listdir(source_dir) if file_.lower().endswith(file_ext.lower())]

    print("\nCopying '{2}' file(s) from\n\t{0}\nto\n\t{1}\nstarting...".format(source_dir, target_dir, file_description))
    [copy_file(file_) for file_ in files]
    print('\nAll done! {0} file(s) have been copied.\n'.format(str(len(files))))

def dirs_exist (dirs):
    """ check if all of the directories exist """

    def dir_exists(dir_):
        exists = os.path.exists(dir_)
        if not exists:
            print('-' * 100 + "\nDirectory \n\t{0}\ndoes not exist! Is device mounted?\n".format(dir_))
        return exists

    return all([dir_exists(dir_) for dir_ in dirs])
