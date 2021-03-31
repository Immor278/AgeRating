# misc.py

import datetime
import os

def get_date():
    date = datetime.datetime.now()
    return date.strftime("%d") + date.strftime("%b") + date.strftime("%Y")

def rename_folder_by_size(folder_path, n):
    new_name = folder_path + '_' + str(n)
    os.rename(folder_path, new_name)
    print('Rename the folder as ', new_name)

def get_n_files(folder_path):
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        return len(filenames)