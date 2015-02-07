#-*- encoding:utf-8 -*-
import os.path
import re
from collections import Counter
import numpy as np
import scipy as sp
import matplotlib.pyplot as pp
import pyhash

# A split function
PAUSE = '<PAUSE>'
STOP = '<STOP>'
def split(file_path):
    CORPUS_PATH = '/Users/nicolas/Data/nlp'
    WORD_RE = '[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàéèêïœç\-]+'
    PAUSE_RE = '[,;:]'
    STOP_RE = '[.?!]'
    ELEMENT_RE = '('+WORD_RE+')|('+PAUSE_RE+')|('+STOP_RE+')'
    with open(os.path.join(CORPUS_PATH,file_path)) as text_file:
        for line in text_file:
            for element in re.finditer(ELEMENT_RE, line):
                if element.group(1):
                    yield element.group(1)
                elif element.group(2):
                    yield PAUSE
                elif element.group(3):
                    yield STOP

# All the triplets are stored
triplets = Counter()

class Feature(object):
    def __init__(self, vocabulary_size=500, feature_size=1000):
        self.hash = pyhash.murmur3_32()
        self.vocabulary_size = vocabulary_size
        self.feature_size = feature_size
        self.threshold = 100
        self.features = {}
        self.counts = {}
    # A feature is updated
    def add_feature(self, word, context):
        i = self.hash(context) % self.feature_size
        try:
            self.features[word][i] += 1
            self.counts[word] += 1
        except:
            self.features[word] = np.zeros(self.feature_size)
            self.features[word][i] += 1
            self.counts[word] = 1
    # Return the sorted list of words
    def get_words(self):
        return sorted(self.features, key=lambda k:-self.counts[k])[:self.vocabulary_size]
    # Get the features matrix
    def get_features(self):
        words = self.get_words()
        features = np.zeros((self.vocabulary_size, self.feature_size))
        for i in xrange(self.vocabulary_size):
            features[i,:] = self.features[words[i]]
        return features
    # Get the counts vector
    def get_counts(self):
        words = self.get_words()
        counts = np.zeros(self.vocabulary_size)
        for i in xrange(self.vocabulary_size):
            counts[i] = self.counts[words[i]]
        return counts

class Context(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.last_last_word = STOP
        self.last_word = STOP
        self.word = STOP
    # Add a word to the context
    def add(self, word):
        self.last_last_word = self.last_word
        self.last_word = self.word
        self.word = word
        self.add_feature(word, '_'.join((self.last_last_word, self.word)))    

ctx = Context()

i = 0
for word in split('frwikisource-20141228-pages-meta-current.xml'):
    i+=1
    if i % 1000000 == 0:
        print i
    ctx.add(word)
    
