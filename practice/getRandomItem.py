"""
get random line item from a file
"""

import random

# filename containing list of items
items_filename = "<REPLACE WITH ITEMS FILE NAME>"

# full filepath name depends on os file system
is_ios_pythonista = True

try:
    import editor
except ImportError:
    is_ios_pythonista = False

# ios generates unique filepath names even if files are in same directory
# therefore get path of current script file and replace its part
# with filepath part of 'items' file
if is_ios_pythonista:
    items_filepath_part = "<REPLACE WITH IOS FILEPATH PART>" # for example, similar to "Ef4IwSN7ket....dEin5D==/"
    this_script_filepath = editor.get_path().split("local-storage/")[1]
    items_filename = editor.get_path().replace(
        this_script_filepath,
        f"{items_filepath_part}{items_filename.lower()}")

# load items from file
with open(items_filename, 'r') as f:
    lines = [line.strip() for line in f.readlines()[1:]] # exclude header line

items = [line for line in lines if line != ""]

# select random item
random_item = random.choice(items)

print(random_item)
