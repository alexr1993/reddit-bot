## This file is as part of the ref bot project

"""
Tools for reading corpora from disk and converting them into feature vectors
"""
import collections
from pprint import pprint
from os import listdir
import re

def read_corpus_from_file(path):
    '''Accepts location of txt file, returns list of words in the file'''
    f = open(path, 'r')
    contents = f.read()

    # split on whitespace
    corpus = re.split('\s+', contents)

    return corpus

def augment_features(counter):
    '''
    Normalises features of input vector such that the values are not
    proportional to the size of the corpus

    vector is a collections.Counter
    '''
    # use highest frequency as a statistic
    most_common = counter.most_common(1)[0][1]

    for word in counter:

        # got this formula from wikipedia Tf-idf augmented frequency
        # roughly
        counter[word] *= (1 / most_common)
        #counter[word] += 0.5


    return counter

def reduce_dimensionality(list_of_vectors):
    '''
    Returns a list of feature vectors all representing the same word
    frequency distribution from each corpus given as an argument.
    If any input corpora do not have words which are selected they will be
    set to zero
    '''

    # This will involve going through the whole sum of corpora and finding
    # the 50 highest scoring words, then reducing each corpus to only
    # those words


    return list_of_vectors

def create_feature_vector(corpus):
    '''
    Accepts list of words, creates feature vector based on normalised
    frequency distribution
    '''
    counter = collections.Counter(corpus)

    # normalise vector using corpus statistics
    counter = augment_features(counter)

    vector = dict(counter) # extra f'nality of counter not needed now

    corpus_length = len(corpus)
    vocabulary_size = len(counter)


    feat_vec = [(word, vector[word]) for word in vector]
    feat_vec.sort() # want in dictionary order


    return feat_vec

# sudo python3.3 corpus_preprocessor.py '/media/alex/Hitachi/raw_data/generic_corpora/
if __name__ == "__main__":

    import sys
    path = sys.argv[1]

    ## Read in all downloaded corpora
    files = [f for f in listdir(path) if re.match('.*.txt', f)]

    pprint(files)

    ## Need to create vectors for each word in thread, the value is the
    #  fraction of the corpus the word takes up

    corpus1 = read_corpus_from_file(path + files[0])

    vec = create_feature_vector(corpus1)

    # useful for viewing vec in order 
    # pprint(sorted(vec, key=lambda word: word[1]))

    #########################################################################

    import readline # optional, will allow Up/Down/History in the console
    import code
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

