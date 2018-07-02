#!/usr/bin/env python

"""
generate a mulitplication times table
"""

import sys
import argparse

# command line args
parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-m", "--max-column-row",
                    help="maximum column and row size (default of 11)", default="11")
args = parser.parse_args()


# verify args
if args.max_column_row.isdigit():
    max_column_row = int(args.max_column_row)
else:
    print("arg 'max-column-row' is not an int: {0}".format(args.max_column_row))
    sys.exit()

column_range = range(0, max_column_row + 1)
row_length = 5 * (max_column_row + 2)

# title
print('')
print('*' * row_length)
print('multiplication table'.center(row_length))
print('*' * row_length)

# first header row
row = '{:>3}'.format('X')
for number in column_range:
	row += '| {:>3}'.format(number)
print(row + '|')
print('-' * row_length)

# grid
for number in column_range:
	row = '{:>3}'.format(number)
	for other_number in column_range:
		row += '| {:>3}'.format(str(number * other_number))
	
	print(row + '|')

print(' ')
