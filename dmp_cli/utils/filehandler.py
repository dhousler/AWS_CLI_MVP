import re
import glob
from pathlib import Path


def file_handler(file):

    file_list = []

    '''search for wildcard * if none found add file to the list'''
    if re.search("\*", file):  # search on the asterisk for wildcard files
        # print(f'Wildcard: {file}')
        for wildcard in glob.glob(file):  # collect all files for wildcards
            # print(f'  {wildcard}')
            file_list += [wildcard]
    else:
        # print(f'Standard files:\n  {file}')
        file_list += [file]  # collect all files for non-wildcards

    return file_list


def directory_handler(directory_list):

    file_list = []

    for directory in directory_list:
        # print(f'Directory: {directory}')

        for path in Path(directory).glob("**/*.*"):  # ** means recursive *.* all files with a . extension
            # print(f'  {path}')
            file_list += [path]

    return file_list


def get_file_contents(file_name):

    with open(file_name, 'r') as infile:

        lines = infile.readlines()
        # print(lines)

    return lines



