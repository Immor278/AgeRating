# permission_ayalyzer.py

import os
import pickle

def analyze_manifest(a):   
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
                permDic[permItem[0]].append(perm)
            else:
                permDic["others"].append(perm)
        else:
            permDic["others"].append(perm)

    result = {
        'App name': app_name,
        'Package name': package_name,
        'Dangerous permissions': permDic["dangerous"],
        'Signature and system permissions': permDic["signature"] + permDic["signatureOrSystem"],
        'Normal permissions': permDic["normal"],
        'Custom permissions': permDic["others"]
    }

    return result