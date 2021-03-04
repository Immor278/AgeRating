# hash_list_checker.py

import hashlib
import os

def hash_apk(apk_path):
    with open(apk_path, "rb") as apk:
        md5Hash = hashlib.md5(apk.read()).hexdigest()
        return md5Hash

def is_hash_existed(hash_value, list_path):
    with open(list_path, "r", encoding="utf8") as list:
        if hash_value in list.read():
            return True

def update_hash_list(apk, list_path):
    md5 = hash_apk(apk)
    if os.path.exists(list_path) and is_hash_existed(md5, list_path):
        print("apk existed: " + apk.split(os.path.sep)[-1])
    else:
        # print("write: "  + apk.split(os.path.sep)[-1])
        with open(list_path, "a", encoding="utf8") as list:
            list.write(str(md5) + '\t' + apk.split(os.path.sep)[-1] + "\n")
            return True

def main():
    folder = "Education_11Feb2021_184"
    path = "C:\\Age_Rating\\App_downloader\\Downloads\\" + folder + "\\APKs\\"
    list_path = "C:\\Age_Rating\\App_downloader\\Downloads\\Hash_list\\hash_list.txt"

    for (dirpath, dirnames, filenames) in os.walk(path):
        for name in filenames:
            apk_path = os.path.join(dirpath, name)
            update_hash_list(apk_path, list_path)

if __name__ == "__main__":
    main()