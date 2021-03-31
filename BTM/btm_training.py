# btm_training.py

import numpy as np
import argparse
import pickle
import random
from biterm.btm import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from biterm.utility import vec_to_biterms

def select_samples(sample_path, num):
    # Randomly select training samples
    texts = open(sample_path,encoding="utf8").read().splitlines()
    if num == -1:
        num = len(texts)
    if num < len(texts):
        texts = random.sample(texts, num)
    print('Set size of training sets as: ' + str(num) + '.')

    return texts

def create_btm(texts, vcb=None, num_topics=20, min_df=0.0001, max_df=0.05):
    # Vectorize texts
    vec = CountVectorizer(stop_words='english', min_df=0.0001, max_df=0.05, vocabulary=vcb)
    X = np.array(vec.fit_transform(texts).toarray())

    # Get vocabulary
    vocab = np.array(vec.get_feature_names())

    # Get biterms
    biterms = vec_to_biterms(X)

    # Create btm
    btm = oBTM(num_topics=num_topics, V=vocab)
 
    return btm, biterms, X, vocab

def train_online_btm(btm, biterms, chunk_size):
    print("Train Online BTM for {} rounds ..".format(int(len(biterms)) / chunk_size))
    for i in range(0, int(len(biterms)), chunk_size): 
        biterms_chunk = biterms[i:i + chunk_size]
        btm.fit(biterms_chunk, iterations=50)

    return btm

def save_pickle(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', metavar='N_REVIEWS', type=int, default=1000, help='The number of training reviews to be loaded.')
    parser.add_argument('-t', metavar='N_TOPICS', type=int, default=20, help='The number of topics.')
    parser.add_argument('-s', metavar='CHUNK_SIZE', type=int, default=100, help='Size of online learning chunk.')
    parser.add_argument('-o', metavar='OUTPUT_FILENAME', type=str, default='btm', help='Filename of output file.')
    parser.add_argument('-p', metavar='SAMPLE_PATH', type=str, default='./data/comments.txt', help='Path to comments.')

    args = parser.parse_args()

    num = args.n
    num_topics = args.t
    chunk_size = args.s
    filename = args.o + '_' + str(num) + '_' + str(num_topics)
    sample_path = args.p

    data_set = select_samples(sample_path, num)
    btm, biterms, _, vocab = create_btm(data_set, num_topics=num_topics, min_df=0.0001, max_df=0.05)
    model = train_online_btm(btm, biterms, chunk_size)

    save_pickle(model, filename + '.mdl')
    save_pickle(vocab, filename + '.vcb')

if __name__ == "__main__":
    main()

