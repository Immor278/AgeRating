# android_guard_analyzer.py

import os
import yaml
import pickle

from androguard.core.bytecodes import apk
from androguard.misc import AnalyzeAPK, Analysis, get_default_session

def androidguard_analyze(apk):
    a, df, dx = AnalyzeAPK(apk)

    print(a)

    output_folder = os.path.join(os.path.dirname(__file__), "androidguard")
    if not os.path.exists(output_folder) or not os.path.isdir(output_folder):
        os.makedirs(output_folder, 0o777, True)
    with open(os.path.join(output_folder, apk.split(os.path.sep)[-1] + '.a'), 'wb') as file:
        pickle.dump(a, file)

apk_folder = 'C:\\Age_Rating\\App_downloader\\Downloads\\' + 'Try' + '\\APKs'

for (dirpath, dirnames, filenames) in os.walk(apk_folder):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        androidguard_analyze(filepath)