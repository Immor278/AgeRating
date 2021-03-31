# static_analyzer.py

import os
import json
import sys

from permission_ayalyzer import analyze_manifest
from lib_analyzer import analyze_lib
from tracker_analyzer import analyze_tracker
from androguard.misc import AnalyzeAPK

def merge(dict1, dict2, dict3):
    res = {**dict1, **dict2, **dict3}
    return res

def static_analyze(apk_folder):
    counter = 0
    output_folder = os.path.join(os.path.dirname(apk_folder), "Static_results")
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for (dirpath, dirnames, filenames) in os.walk(apk_folder):
        for filename in filenames: 
            counter += 1
            json_path = os.path.join(output_folder, filename + '.json')
            if not os.path.exists(json_path):
                print('Analyzing #' + str(counter) + ': ' + os.path.join(dirpath, filename))
                
                a, df, dx = AnalyzeAPK(os.path.join(dirpath, filename)) 
                permission_result = analyze_manifest(a)
                tracker_result = analyze_tracker(dx)
                lib_result = {"LibRadar": analyze_lib(os.path.join(dirpath, filename))}

                result = merge(permission_result, tracker_result, lib_result)

                with open(json_path, "w+", encoding="utf8") as f_json:
                    json.dump(result, f_json)
            else:
                print('#' + str(counter) + ': ' + os.path.join(dirpath, filename) + 'already tested.')

def static_analyze_all(top_folder):
    for (dirpath, dirnames, filenames) in os.walk(top_folder):
        if dirpath.split(os.path.sep)[-1] == "APKs":
            clean_temp_files()
            static_analyze(dirpath)

def clean_temp_files():
    literadar_log = r"C:\Age_Rating\Static_analysis\log_libradar.txt"
    literadar_decompile_folder = r"C:\Age_Rating\LiteRadar\LiteRadar\Data\Decompiled"
    os.remove(literadar_log)
    os.remove(literadar_decompile_folder)

def main():
    top_folder = sys.argv[1]
    
    
    static_analyze_all(top_folder)

if __name__ == "__main__":
    main()