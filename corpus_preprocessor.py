## This file is as part of the ref bot project
from thread_scraper import write_corpus_to_file

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
    f.close()
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

def reduce_dimensionality(vector, schema):
    '''
    Really simple dimensionality reduction - remove all words in vector which
    are not in the schema

    vector : list of [word, frequency]
    schema : list of words
    '''

    # This will involve going through the whole sum of corpora and finding
    # the 50 highest scoring words, then reducing each corpus to only
    # those words
    vector = [word for word in vector if word[0] in schema]

    non_occuring_words = set(schema).difference(set(dict(vector)))
    non_occuring_words = [(word, 0) for word in non_occuring_words]


    vector += list(non_occuring_words)


    return sorted(vector)

def create_feature_vector(corpus):
    '''
    Accepts list of words, creates feature vector based on normalised
    frequency distribution
    '''
    counter = collections.Counter(corpus)

    # normalise vector using corpus statistics
    dictionary = augment_features(counter)

    vector = dict(counter) # extra f'nality of counter not needed now

    corpus_length = len(corpus)
    vocabulary_size = len(counter)


    feat_vec = [(word, dictionary[word]) for word in dictionary]
    feat_vec.sort() # want in dictionary order

    return feat_vec

def create_vocabulary_schema(feature_vecs, dimensionality):
    '''
    Create a schema of a given dimensionality based on a list of feature
    vectors. The highest scoring words will be put in the schema

    feature_vecs : list of feature vectos [[word1,freq1],...,[wordm,freqm]]
        sorted in alphabetical order
    dimensionality : number of words the output schema will contain

    This function assumes all vectors features have been normalised - ie they
    have the same scale
    '''
    total_counter = collections.Counter()

    for vec in feature_vecs:
        # remove words under 3 letters cos they're noise
        vec = [word for word in vec if len(word[0]) > 3]

        counter = collections.Counter(dict(vec))
        total_counter += counter

    schema = list(dict(total_counter.most_common(dimensionality)))

    return schema

def create_schema_using_directory(dir, name):
    '''
    dir : path to a directory containing 1 or more corpora
    dimensionality : K value for output schema

    schema is written to SCHEMA_PATH/name.txt

    dir must have a folder named 'training' containing th corpora
    '''
    path = '/'.join([DATA_ROOT, dir, 'training'])

    files = [f for f in listdir(path) if re.match('.*.txt', f)]

    vectors = []

    for file in files:
        corpus = read_corpus_from_file('/'.join([path, file]))
        vec = create_feature_vector(corpus)
        vectors.append(vec)

    schema = create_vocabulary_schema(vectors, K)

    write_corpus_to_file(schema, '/'.join([SCHEMA_PATH, name + '.txt']))
    print("Created schema " + name + " in " + SCHEMA_PATH)

def create_feature_vector_set(dir, schema_name):
    '''
    dir : e.g. generic_corpora/training
    schema : e.g. banana
    '''
    schema = read_corpus_from_file('/'.join([SCHEMA_PATH,\
        schema_name + '.txt']))

    files = listdir('/'.join([DATA_ROOT, dir]))

    vectors = []

    for file in files:
        corpus = read_corpus_from_file('/'.join([DATA_ROOT, dir, file]))
        vec = create_feature_vector(corpus)
        vec = reduce_dimensionality(vec, schema)

        # finally strip words away so a vector of numbers remains
        vec = [pair[1] for pair in vec]

        vectors.append(vec)
    return vectors

global DATA_ROOT
global SCHEMA_PATH
global K

if __name__ == "__main__":

    import sys
    topic = sys.argv[1]
    data_set = sys.argv[2]

    DATA_ROOT = '/media/alex/Hitachi/raw_data'
    SCHEMA_PATH = '/'.join([DATA_ROOT, 'topic_schemas'])
    K = 100

    ## Read in all downloaded corpora
    files = [f for f in listdir('/'.join([DATA_ROOT, topic, data_set])) \
        if re.match('.*.txt', f)]

    pprint(files)

    create_schema_using_directory('banana_for_scale_corpora', 'banana')
    create_schema_using_directory('generic_corpora','generic')

    ## Create feature vectors ready for training/testing
    banana_training_vecs = create_feature_vector_set('banana_for_scale_corpora/training', 'banana')
    generic_training_vecs = create_feature_vector_set('generic_corpora/training', 'generic')

    # cross validation data found by surfing reddit not in search
    banana_cv_vecs = create_feature_vector_set('banana_for_scale_corpora/cv', 'banana')

    banana_test_vecs = create_feature_vector_set('banana_for_scale_corpora/test', 'banana')
    generic_test_vecs = create_feature_vector_set('generic_corpora/test', 'generic')

    

    ## BUILD A CLASSIFIER FROM THIS PREPROCESSED DATA - THIS CODE SHOULD SOON BE MOVED
    #  TO ANOTHER FILE
    import numpy as np
    X = banana_training_vecs + generic_training_vecs # concat all training data
    # create list of labels
    y = [1 for x in banana_training_vecs] + [0 for x in generic_training_vecs]

    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB()
    clf.fit(X,y)
    print(clf.predict(generic_test_vecs[0])) # should be 0 for all generic vecs


    # useful for viewing vec in order 
    # pprint(sorted(vec, key=lambda word: word[1]))

    #########################################################################

    import readline # optional, will allow Up/Down/History in the console
    import code
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()


