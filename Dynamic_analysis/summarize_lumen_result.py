# summarize_lumen_result.py

import sqlite3
import os

def importdb(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        privacy = list(c.execute('SELECT app_package, app_name, pii_type from privacy_table'))
        flow = list(c.execute('SELECT app_package, app_name, sink_dns_fqdn from passive_table'))
    except sqlite3.Error as e:
        print(e)
    return privacy, flow

def is_value_existed(value, file):
    with open(file, "r", encoding="utf8") as f:
        if value in f.read():
            return True

def to_str_list(list, sp):
    new_list = []
    for tuple in list:
        str = sp.join(tuple)
        new_list.append(str)
    return new_list

def write_to_file(list, output_path):
    for line in list:
        if not os.path.exists(output_path):
            with open(output_path, "w+", encoding='utf8') as out_f:
                out_f.write(line + '\n')
        else:
            if not is_value_existed(line, output_path):
                with open(output_path, "a", encoding='utf8') as out_f:
                    out_f.write(line + '\n')

def summarize_db(db, output_folder):
    sp = '||'
    privacy, flow = importdb(db)
    write_to_file(to_str_list(privacy, sp), os.path.join(output_folder, r'lumen_privacy.txt'))
    write_to_file(to_str_list(flow, sp), os.path.join(output_folder, r'lumen_flow.txt'))

def summarize_all_db(top_folder):
    for (dirpath, dirnames, filenames) in os.walk(top_folder):
        for filename in filenames:
            if filename.endswith('db') and filename.startswith('lumen'):
                print(os.path.join(dirpath, filename))
                summarize_db(os.path.join(dirpath, filename), top_folder)

def main():
    output_folder = r'C:\Age_Rating'
    top_folder = r'C:\Age_Rating\Apk\Testing'
    # db = r"C:\Age_Rating\Dynamic_analysis\haystack.db"
    
    summarize_all_db(top_folder)

if __name__ == "__main__":
    main()