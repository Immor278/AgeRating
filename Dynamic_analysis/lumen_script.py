import os
import argparse
import sys
import subprocess
import time

def lumen_test(apk_folder, device):
    lumen = "edu.berkeley.icsi.haystack"
    log = os.path.join(apk_folder, 'Lumen_log.txt')
    if not os.path.exists(log):
        with open(log, 'w+'): pass

    big_counter = 0
    for (dirpath, dirnames, filenames) in os.walk(apk_folder):
        if dirpath.endswith('APKs'):
            counter = 0
            for filename in filenames:
                if os.path.splitext(filename)[-1] == '.apk':
                    apk_path = os.path.join(dirpath, filename)
                    package_name = filename.split(' ')[-1][:-4]
                    counter += 1
                    if not is_tested(log, package_name):
                        if is_app_running(lumen, device):
                            print('# ' + str(counter) + ' ' + package_name + ' starts testing ...\n')
                            os.system('adb -s ' + device + ' install "' + apk_path + '"')
                            time.sleep(5)
                            os.system('adb -s ' + device + ' shell monkey -p ' + package_name + ' -c android.intent.category.LAUNCHER 1')
                            time.sleep(180)
                            os.system('adb -s ' + device + ' shell am force-stop ' + package_name)
                            time.sleep(1)
                            os.system('adb -s ' + device + ' uninstall "' + package_name + '"')
                            time.sleep(1)
                            write_to_log(package_name + '\n', log)

                            if counter % 10 == 0:
                                os.system('adb -s ' + device + ' pull /data/data/edu.berkeley.icsi.haystack/databases/haystack.db ' + get_out_db_path(dirpath, counter))
                        else:
                            print('Lumen is not running. Stop testing at ', os.path.join(dirpath, filename))
                            sys.exit(0)
                    else:
                        print('# ' + str(counter) + ' ' + package_name + ' has been tested.')
            print('End of test.')
            os.system('adb -s ' + device + ' pull /data/data/edu.berkeley.icsi.haystack/databases/haystack.db ' + get_out_db_path(dirpath, counter))

def get_out_db_path(dirpath, counter):
    return os.path.join(os.path.dirname(dirpath), "lumen_" + str(counter) + '.db')

def is_tested(log, package_name):
    with open(log, "r+") as log_f:
        if package_name in log_f.read():
            return True

def is_app_running(package_name, device):
    cmd = "adb -s " + device + " shell pidof " + package_name
    try:
        result = subprocess.check_output(cmd, shell=True)
    except:
        return False
    return True

def write_to_log(message, log):
    with open(log, "a+") as log_f:
        log_f.write(message)


def main():
    apk_folder = sys.argv[1]
    device = sys.argv[2]

    lumen_test(apk_folder, device)

if __name__ == "__main__":
    main()
