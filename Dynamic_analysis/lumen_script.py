import os
import time
import argparse

def lumen_test(apk_folder):
    for (dirpath, dirnames, filenames) in os.walk(apk_folder):
        for name in filenames:
            apk_path = os.path.join(dirpath, name)
            print(apk_path)
            package_name = name.split(' ')[-1][:-4]
            print(package_name)
            os.system('adb install "' + apk_path + '"')
            time.sleep(1)
            os.system('adb shell monkey -p ' + package_name + ' -c android.intent.category.LAUNCHER 1')
            time.sleep(60)
            os.system('adb shell am force-stop ' + package_name)
            time.sleep(1)
            os.system('adb uninstall "' + package_name + '"')
            time.sleep(1)

def main():
    apk_folder = 'C:\\Age_Rating\\App_downloader\\Downloads\\Family_TopFree_11Feb2021_161\APKs\\'
    lumen_test(apk_folder)

if __name__ == "__main__":
    main()
