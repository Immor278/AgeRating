# btm_cluster_assign.py

import numpy as np
import random
# import pyLDAvis
import argparse
import pickle
from biterm.btm import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from biterm.utility import vec_to_biterms, topic_summuary

path = "C:\\Age_Rating\\App_downloader\\BTM\\"

parser = argparse.ArgumentParser()
parser.add_argument('-n', metavar='number', type=int, default=10000, help='The number of input reviews.')
parser.add_argument('-f', metavar='filename', type=str, required=True, help='filename of btm obj and vocabulary files.')

args = parser.parse_args()

num = args.n
filename = args.f

# Randomly select training samples
texts = open('./data/comments.txt',encoding="utf8").read().splitlines()
if num == -1:
    num = len(texts)
if num < len(texts):
    texts = random.sample(texts, num)
print('Set size of input sets as: ' + str(num) + '.')


with open(filename + '.vcb','rb') as file_vcb:
    vcb = pickle.load(file_vcb)

with open(filename + '.obj','rb') as file_btm:
    btm = pickle.load(file_btm)

# vectorize texts
vec = CountVectorizer(vocabulary=vcb)
# # ,min_df=0.0001,max_df=0.05
# # X = vec.fit_transform(texts).toarray()
X = np.array(vec.fit_transform(texts).toarray())
# # print(X)

# print('get vocabulary')
# vocab = np.array(vec.get_feature_names())

# # print(vocab[:500])
# # print(len(vocab))

# print('get biterms')
biterms = vec_to_biterms(X)

# print('create btm')
# btm = oBTM(num_topics=30, V=vcb)

# print("\n\n Train Online BTM ..")
# for i in range(0, int(len(biterms)), 100): # prozess chunk of 200 texts
#     biterms_chunk = biterms[i:i + 100]
#     btm.fit(biterms_chunk, iterations=50)
# # biterms_chunk = biterms[:n]
# # btm.fit(biterms_chunk, iterations=50)

# object_btm = btm
# file_btm_obj = open('btm.obj', 'wb') 
# pickle.dump(object_btm, file_btm_obj)

# file_btm_obj = open('btm.obj','rb') 
# btm = pickle.load(file_btm_obj)

topics = btm.transform(biterms)

# print("\n\n Visualize Topics ..")
# vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(X, axis=1), vocab, np.sum(X, axis=0))
# # pyLDAvis.save_html(vis, './vis/online_btm_' + str(n) + '.html')
# pyLDAvis.save_html(vis, './vis/online_btm_' + 'online_all2' + '.html')

print("\n\n Topic coherence ..")
topic_summuary(btm.phi_wz.T, X, vcb, 20)

print("\n\n Texts & Topics ..")

for k in range(3):
    j = 0
    for i in range(len(texts)):
        if topics[i].argmax() == k:
            print("{} (topic: {})".format(texts[i], topics[i].argmax()))
            j += 1
            if j > 10:
                break
