# summarize_static_analysis.py
import sys
import os
import json
import pickle

def summarize(top_folder):
    sp = '||'
    txt_path = os.path.join(top_folder, 'static_results.txt')
    if os.path.exists(txt_path):
        os.remove(txt_path)

    permission_list_path = os.path.join(os.path.dirname(__file__), "dvm_permission.lst")
    permission_list = pickle.load(open(permission_list_path,'rb'))

    dangerous_permissions, signature_permissions, trackers, permissions_without_requiring = init_pools(top_folder, permission_list)
    str_ = 'Apk Name' + sp + perms_to_str(dangerous_permissions, sp) + sp + perms_to_str(signature_permissions, sp) + sp + perms_to_str(permissions_without_requiring, sp) + sp + sp.join(trackers)
    write_to_txt(str_ + '\n', txt_path)

    for (dirpath, dirnames, filenames) in os.walk(top_folder):
        for filename in filenames: 
            if dirpath.split(os.path.sep)[-1] == "Static_results" and os.path.splitext(filename)[-1] == '.json':
                txt_path = os.path.join(top_folder, 'static_results.txt')
                results = []
                json_path = os.path.join(dirpath, filename)
                with open(json_path, "r") as json_f:
                    static_result = json.load(json_f)
                    results.append(static_result['Package name'])
                    results.append(arr_to_sp_str(convert_to_zero_one(static_result['Dangerous permissions'], dangerous_permissions), sp))
                    results.append(arr_to_sp_str(convert_to_zero_one(static_result['Signature and system permissions'], signature_permissions), sp))
                    
                    lib_results = []
                    for lib in static_result['LibRadar']:
                        if 'Permission' in lib.keys():
                            perm_arr = []
                            for perm in lib['Permission']:
                                if not is_perm_required(perm, static_result):
                                    perm_arr.append(perm)
                            lib_results.append(convert_to_zero_one(perm_arr, permissions_without_requiring))
                    if len(lib_results) == 0:
                        lib_results = ['0'] * len(permissions_without_requiring)
                        results.append(sp.join(lib_results) + sp)
                    else:
                        results.append(arr_to_sp_str(convert_to_zero_one_accumulate(lib_results), sp))
                    results.append(arr_to_sp_str(convert_to_zero_one(static_result['Trackers'], trackers), sp))
                    str_ = sp.join(results)
                write_to_txt(str_ + '\n', txt_path)          

def write_to_txt(content, txt_path):
    with open(txt_path, "a+") as txt_f:
        txt_f.write(content)

def init_pools(top_folder, permission_list):
    dangerous_permissions = []
    signature_permissions = []
    trackers = []
    permissions_without_requiring = []

    for (dirpath, dirnames, filenames) in os.walk(top_folder):
        for filename in filenames: 
            if dirpath.split(os.path.sep)[-1] == "Static_results" and os.path.splitext(filename)[-1] == '.json':
                txt_path = os.path.join(top_folder, 'static_results.txt')
                json_path = os.path.join(dirpath, filename)
                with open(json_path, "r") as json_f:
                    static_result = json.load(json_f)
                    add_new_items(static_result['Dangerous permissions'], dangerous_permissions)
                    add_new_items(static_result['Signature and system permissions'], signature_permissions)
                    add_new_items(static_result['Trackers'], trackers)

                    for lib in static_result['LibRadar']:
                        if 'Permission' in lib.keys():
                            for perm in lib['Permission']:
                                if is_perm_danger(perm, permission_list):
                                    add_new_item(perm, permissions_without_requiring)

    return dangerous_permissions, signature_permissions, trackers, permissions_without_requiring

def is_perm_danger(perm, permission_list):
    if perm.startswith("android.permission"):
        permSuffix = perm.split('.')[-1]
        if permSuffix in permission_list['MANIFEST_PERMISSION']:
            permItem = permission_list["MANIFEST_PERMISSION"][permSuffix]
            if permItem[0] == 'dangerous':
                return True

def is_perm_required(perm, json_obj):
    required_perms = json_obj['Dangerous permissions'] + json_obj['Signature and system permissions']
    return perm in required_perms

def perms_to_str(perms, sp):
    perm_str = []
    for permission in perms:
        permission = permission.split('.')[-1]
        perm_str.append(permission)
    return sp.join(perm_str) + sp

def convert_to_zero_one(items, pool):
    out = []
    for item in pool:
        if item in items:
            out.append(1)
        else:
            out.append(0)
    return out

def convert_to_zero_one_accumulate(items):
    out = []
    if len(items) != 0:
        out = [0] * len(items[0])

    for i in range(len(items)):
        for j in range(len(items[0])):
            out[j] += items[i][j]
            
    for i in range(len(out)):
        if out[i] > 0:
            out[i] = 1
    return out

def arr_to_sp_str(arr, sp):
    arr = map(str, arr)
    return sp.join(arr) + sp

def add_new_item(item, pool):
    if item not in pool:
        pool.append(item)

def add_new_items(items, pool):
    for item in items:
        add_new_item(item, pool)

def main():
    top_folder = sys.argv[1]
    summarize(top_folder)

if __name__ == "__main__":
    main()