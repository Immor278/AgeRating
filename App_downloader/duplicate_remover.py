# duplicate_remover.py

import os
import sys
from hash_list_checker import update_hash_list

def remove_duplicate(folder, hash_list):
    for (dirpath, dirnames, filenames) in os.walk(folder):
        for name in filenames:
            apk_path = os.path.join(dirpath, name)
            if not update_hash_list(apk_path, hash_list):
                os.remove(apk_path)
                print("apk removed")

def main():
    folder = sys.argv[1]
    path = "C:\\Age_Rating\\App_downloader\\Downloads\\" + folder + "\\APKs\\"
    hash_list = "C:\\Age_Rating\\App_downloader\\Downloads\\Hash_list\\hash_list.txt"

    remove_duplicate(path, hash_list)

if __name__ == "__main__":
    main()