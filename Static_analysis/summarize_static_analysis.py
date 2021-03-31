# summarize_static_analysis.py
import sys
import os
import json
import pickle

class Summarize_static_analysis:
    top_folder = ''
    sp = '||'
    dangerous_permissions = []
    signature_permissions = []
    trackers = []
    permissions_without_requiring = []

    def __init__(self, top_folder):
        self.top_folder = top_folder
        self.permission_list = self.get_permission_list()
        self.txt_path = os.path.join(self.top_folder, 'static_results.txt')

    def get_permission_list(self):
        permission_list_path = os.path.join(os.path.dirname(__file__), "dvm_permission.lst")
        return pickle.load(open(permission_list_path,'rb'))

    def write_header(self):
        self.init_pools()
        strings = []
        strings.append('Apk Name')
        strings.append(self.perms_to_str(self.dangerous_permissions))
        strings.append(self.perms_to_str(self.signature_permissions))
        strings.append(self.perms_to_str(self.permissions_without_requiring))
        strings.append(self.sp.join(self.trackers))
        self.write_to_txt(self.sp.join(strings) + '\n')

    def write_resutls(self):
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            for filename in filenames: 
                if dirpath.split(os.path.sep)[-1] == "Static_results" and os.path.splitext(filename)[-1] == '.json':
                    results = []
                    json_path = os.path.join(dirpath, filename)
                    with open(json_path, "r") as json_f:
                        static_result = json.load(json_f)
                        results.append(static_result['Package name'])
                        results.append(self.arr_to_sp_str(self.convert_to_zero_one(static_result['Dangerous permissions'], self.dangerous_permissions)))
                        results.append(self.arr_to_sp_str(self.convert_to_zero_one(static_result['Signature and system permissions'], self.signature_permissions)))
                        
                        lib_results = []
                        for lib in static_result['LibRadar']:
                            if 'Permission' in lib.keys():
                                perm_arr = []
                                for perm in lib['Permission']:
                                    if not self.is_perm_required(perm, static_result):
                                        perm_arr.append(perm)
                                lib_results.append(self.convert_to_zero_one(perm_arr, self.permissions_without_requiring))
                        if len(lib_results) == 0:
                            lib_results = ['0'] * len(self.permissions_without_requiring)
                            results.append(self.sp.join(lib_results) + self.sp)
                        else:
                            results.append(self.arr_to_sp_str(self.convert_to_zero_one_accumulate(lib_results)))
                        results.append(self.arr_to_sp_str(self.convert_to_zero_one(static_result['Trackers'], self.trackers)))
                        self.write_to_txt(self.sp.join(results) + '\n') 


    def summarize(self):
        if os.path.exists(self.txt_path):
            os.remove(self.txt_path)

        self.write_header()
        self.write_resutls()        

    def write_to_txt(self, content):
        with open(self.txt_path, "a+") as txt_f:
            txt_f.write(content)

    def init_pools(self):
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            for filename in filenames: 
                if dirpath.split(os.path.sep)[-1] == "Static_results" and os.path.splitext(filename)[-1] == '.json':
                    txt_path = os.path.join(self.top_folder, 'static_results.txt')
                    json_path = os.path.join(dirpath, filename)
                    with open(json_path, "r") as json_f:
                        static_result = json.load(json_f)
                        self.add_new_items(static_result['Dangerous permissions'], self.dangerous_permissions)
                        self.add_new_items(static_result['Signature and system permissions'], self.signature_permissions)
                        self.add_new_items(static_result['Trackers'], self.trackers)

                        for lib in static_result['LibRadar']:
                            if 'Permission' in lib.keys():
                                for perm in lib['Permission']:
                                    if self.is_perm_danger(perm):
                                        self.add_new_item(perm, self.permissions_without_requiring)

    def is_perm_danger(self, perm):
        if perm.startswith("android.permission"):
            permSuffix = perm.split('.')[-1]
            if permSuffix in self.permission_list['MANIFEST_PERMISSION']:
                permItem = self.permission_list["MANIFEST_PERMISSION"][permSuffix]
                if permItem[0] == 'dangerous' or permItem[0] == 'signature' or permItem[0] == 'signatureOrSystem':
                    return True

    def is_perm_required(self, perm, json_obj):
        required_perms = json_obj['Dangerous permissions'] + json_obj['Signature and system permissions']
        return perm in required_perms

    def perms_to_str(self, perms):
        perm_str = []
        for permission in perms:
            permission = permission.split('.')[-1]
            perm_str.append(permission)
        return self.sp.join(perm_str) + self.sp

    def convert_to_zero_one(self, items, pool):
        out = []
        for item in pool:
            if item in items:
                out.append(1)
            else:
                out.append(0)
        return out

    def convert_to_zero_one_accumulate(self, items):
        out = []
        if len(items):
            out = [0] * len(items[0])

        for i in range(len(items)):
            for j in range(len(items[0])):
                out[j] += items[i][j]
                
        for i in range(len(out)):
            if out[i] > 0:
                out[i] = 1
        return out

    def arr_to_sp_str(self, arr):
        return self.sp.join(map(str, arr)) + self.sp

    def add_new_item(self, item, pool):
        if item not in pool:
            pool.append(item)

    def add_new_items(self, items, pool):
        for item in items:
            self.add_new_item(item, pool)

def main():
    top_folder = sys.argv[1]
    Summarize_static_analysis(top_folder).summarize()

if __name__ == "__main__":
    main()