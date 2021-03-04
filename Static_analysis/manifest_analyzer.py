# manifest_analyzer.py

import os
import yaml
import pickle

from androguard.core.bytecodes import apk
from androguard.misc import AnalyzeAPK, Analysis, get_default_session

def manifest_analysis(apk):
    a, df, dx = AnalyzeAPK(apk)

    app_name = a.get_app_name()
    package_name = a.get_package()

    permissions = a.get_permissions()

    permDic = {
        "dangerous": [],
        "normal": [],
        "signature": [],
        "signatureOrSystem": [],
        "others": []  # unknown permission
    }

    with open(os.path.join(os.path.dirname(__file__), "dvm_permission.lst"),'rb') as file_permission:
        DVM_PERMISSIONS = pickle.load(file_permission)

    for perm in permissions:
        perm: str = perm
        if perm.startswith("android.permission"):
            permSuffix = perm[len("android.permission") + 1:]
            if permSuffix in DVM_PERMISSIONS["MANIFEST_PERMISSION"]:
                permItem = DVM_PERMISSIONS["MANIFEST_PERMISSION"][permSuffix]
                permDic[permItem[0]].append(permSuffix)
            else:
                permDic["others"].append(permSuffix)
        else:
            permDic["others"].append(perm)

    result = {
        'App name': app_name,
        'Package name': package_name,
        'Dangerous permissions': permDic["dangerous"],
        'Signature and system permissions': permDic["signature"] + permDic["signatureOrSystem"],
        'Custom permissions': permDic["others"]
    }

    return result

apk_folder = 'C:\\Age_Rating\\App_downloader\\Downloads\\' + 'Try' + '\\APKs'
# androidguard_result_folder = 'C:\\Age_Rating\\Static_analysis\\androidguard\\Try'

results = []

for (dirpath, dirnames, filenames) in os.walk(apk_folder):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        # print(filepath)
        # with open(filepath,'rb') as file:
        #     a = pickle.load(file)
        #     print(a)
        #     print(a.get_app_name())
        results.append(manifest_analysis(filepath))
        
output_folder = os.path.join(os.path.dirname(__file__), "results")
if not os.path.exists(output_folder) or not os.path.isdir(output_folder):
    os.makedirs(output_folder, 0o777, True)
with open(os.path.join(output_folder, apk_folder.split(os.path.sep)[-2] + '.per'), 'wb') as file:
    pickle.dump(results, file)


for (dirpath, dirnames, filenames) in os.walk(output_folder):
    for filename in filenames:
        with open(os.path.join(output_folder, filename),'rb') as file_permission:
            perm = pickle.load(file_permission)
            print(perm)