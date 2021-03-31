# script_download_all_categories.py

import os
import sys
import argparse
import datetime
import shutil
from app_review_downloader import obtain_app_list, download_app_and_review, download_app_apkpure
from duplicate_remover import remove_duplicate_apk


def start_download(category, save_path, hash_list):
    app_list = obtain_app_list(category, 'TOP_FREE', '200', save_path)
    download_app_and_review(app_list, '3000', save_path)
    clean_up(category, save_path, hash_list)

def download_from_app_list(app_list, save_path):
    words = app_list.split(os.path.sep)[-1].split('_')[1:-3]
    category = '_'.join(words)

    download_app_and_review(app_list, '3000', save_path)

    hash_list = "C:\\Age_Rating\\Apk\\Apk_list\\apk_list.txt"
    clean_up(category, save_path, hash_list)

def download_from_app_list_apkpure(app_list, save_path):
    words = app_list.split(os.path.sep)[-1].split('_')[1:-3]
    category = '_'.join(words)

    download_app_apkpure(app_list, save_path)

def get_date():
    date = datetime.datetime.now()

    return date.strftime("%d") + date.strftime("%b") + date.strftime("%Y")

def clean_up(category, path, hash_list):   

    save_path = path + category + '_' + 'TOP_FREE_' + get_date()
    os.mkdir(save_path)
    os.mkdir(save_path + '\\APKs')

    if os.path.exists(path + '\\App_list'):
        shutil.move(path + '\\App_list', save_path)
    if os.path.exists(path + '\\Reviews'): 
        shutil.move(path + '\\Reviews', save_path)

    for (dirpath, dirnames, filenames) in os.walk(path):
        for name in filenames:
            apk_path = os.path.join(path, name)
            if os.path.exists(apk_path):
                shutil.move(apk_path, save_path + '\\APKs')
    
    remove_duplicate_apk(save_path + '\\APKs', hash_list)
    rename_folder(save_path + '\\APKs')

def rename_folder(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        n = len(filenames)
    folder_path = os.path.dirname(path)
    os.rename(folder_path, folder_path + '_' + str(n))
    print('Rename the folder as ', folder_path + '_' + str(n))

def main():
    hash_list = "C:\\Age_Rating\\Apk\\Apk_list\\apk_list.txt"
    
    # save_path = "C:\\Age_Rating\\App_downloader\\Family_apk\\ApkPure_apks\\"
    save_path = "C:\\Age_Rating\\App_downloader\\Downloads\\"
    # app_list = "C:\Age_Rating\App_downloader\Downloads\Application_NewFree_1Mar2021_85\App_list\list_APPLICATION_NEW_FREE_1Mar2021_200.json"
    # app_list = sys.argv[1]

    # download_from_app_list(app_list, save_path)
    # download_from_app_list_apkpure(app_list, save_path)

    for category in categories:
        start_download(category, save_path, hash_list)
        

categories = [
    # 'ANDROID_WEAR',
    # 'ART_AND_DESIGN',
    # 'AUTO_AND_VEHICLES',
    # 'BEAUTY',
    # 'BOOKS_AND_REFERENCE',
    # 'BUSINESS',
    # 'COMICS',
    # 'COMMUNICATION',
    # 'DATING',
    'EDUCATION',
    # 'ENTERTAINMENT',
    # 'EVENTS',
    # 'FINANCE',
    # 'FOOD_AND_DRINK',
    # 'HEALTH_AND_FITNESS',
    # 'HOUSE_AND_HOME',
    # 'LIBRARIES_AND_DEMO',
    # 'LIFESTYLE',
    # 'MAPS_AND_NAVIGATION',
    # 'MEDICAL',
    # 'MUSIC_AND_AUDIO',
    # 'NEWS_AND_MAGAZINES',
    # 'PARENTING',
    # 'PERSONALIZATION',
    'PHOTOGRAPHY',
    'PRODUCTIVITY',
    # 'SHOPPING',
    # 'SOCIAL',
    # 'SPORTS',
    # 'TOOLS',
    # 'TRAVEL_AND_LOCAL',
    # 'VIDEO_PLAYERS',
    # 'WEATHER',
    'FAMILY'
    ]

if __name__ == "__main__":
    main()