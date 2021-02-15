import os
import argparse
import json

path = 'C:\\Age_Rating\\App_downloader\\Downloads\\'

parser = argparse.ArgumentParser()
parser.add_argument('-f', metavar='FOLDER_NAME', type=str, required=True,
                        help='The folder name.')
parser.add_argument('-r', metavar='RATING', type=int, default=1,
                        help='The rating given by the reviewer.')             
args = parser.parse_args()

for (dirpath, dirnames, filenames) in os.walk(path + args.f + '\\Reviews'):
    for name in filenames:
        thepath = os.path.join(dirpath, name)
        comments = []
        with open(thepath, "r", encoding="utf8") as load_f:
            load_arr = json.load(load_f)
            for comment in load_arr['data']:
                if comment['score'] == args.r:
                    comments.append(comment['text'])
            with open(path + args.f + '\\comments.txt','a',encoding="utf8") as out_f:
                for line in comments:
                    if line: 
                        out_f.write(line)
                        out_f.write("\n")