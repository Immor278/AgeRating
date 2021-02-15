# btm_training.py

import numpy as np
import argparse
import pickle
import random
# import sklearn
from biterm.btm import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from biterm.utility import vec_to_biterms

path = "C:\\Age_Rating\\App_downloader\\BTM\\"

parser = argparse.ArgumentParser()
parser.add_argument('-n', metavar='N_REVIEWS', type=int, default=1000, help='The number of training reviews to be loaded.')
parser.add_argument('-t', metavar='N_TOPICS', type=int, default=20, help='The number of topics.')
parser.add_argument('-s', metavar='CHUNK_SIZE', type=int, default=100, help='Size of online learning chunk.')
parser.add_argument('-o', metavar='OUTPUT_FILENAME', type=str, default='btm', help='Filename of output file.')

args = parser.parse_args()

num = args.n
num_topics = args.t
chunk_size = args.s
filename = args.o

# Randomly select training samples
texts = open('./data/comments.txt',encoding="utf8").read().splitlines()
if num == -1:
    num = len(texts)
if num < len(texts):
    texts = random.sample(texts, num)
print('Set size of training sets as: ' + str(num) + '.')

    # random.shuffle(texts)
    # test_dataset, training_dataset = sklearn.model_selection.train_test_split(texts, train_size=num, test_size=len(texts)-num)

# Vectorize texts
vec = CountVectorizer(stop_words='english',min_df=0.0001,max_df=0.05)
X = np.array(vec.fit_transform(texts).toarray())

# Get vocabulary
vocab = np.array(vec.get_feature_names())

# Get biterms
biterms = vec_to_biterms(X)

# Create btm
btm = oBTM(num_topics=num_topics, V=vocab)

print("\n\n Train Online BTM ..")
for i in range(0, int(len(biterms)), chunk_size): 
    biterms_chunk = biterms[i:i + chunk_size]
    btm.fit(biterms_chunk, iterations=50)

# print('Save BTM model')
with open(filename + '_' + str(num) + '_' + str(num_topics) + '.mdl', 'wb') as file_btm_obj:
    pickle.dump(btm, file_btm_obj)
    
# print('Save vocabulary')
with open(filename + '_' + str(num) + '_' + str(num_topics) + '.vcb', 'wb') as file_vcb:
    pickle.dump(vocab, file_vcb)

print('done!')