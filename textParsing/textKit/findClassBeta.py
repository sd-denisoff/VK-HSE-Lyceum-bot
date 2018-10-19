from keras.models import load_model
import tensorflow as tf
from keras import backend as K
from nltk.stem.snowball import RussianStemmer
import re
import numpy as np


class findClass:
    PROJECT_NAME = "Baikal"
    START_PATH = "textParsing/models/classifierData/"
    MODEL_PATH = ""
    VOCAB_PATH = ""
    LABELS_PATH = ""
    VOCAB_SIZE = 0
    vocab = []
    token2Index = {}
    index2Label = []
    model = None

    stemer = RussianStemmer()
    regex = re.compile('[^а-яА-Я ]')
    stem_cache = {}

    def _set_path(self):
        self.MODEL_PATH = self.START_PATH + self.PROJECT_NAME + '.h5'
        self.VOCAB_PATH = self.START_PATH + self.PROJECT_NAME + '_vocab.txt'
        self.LABELS_PATH = self.START_PATH + self.PROJECT_NAME + '_labels.txt'

    def _restore_data(self):
        with open(self.VOCAB_PATH, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for line in lines[:len(lines) - 1]:
            line = line.lower()
            self.vocab.append(line)

        self.VOCAB_SIZE = len(self.vocab)
        self.token2Index = {self.vocab[i]: i for i in range(self.VOCAB_SIZE)}

        with open(self.LABELS_PATH, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for line in lines[:len(lines) - 1]:
            line = line.lower()
            self.index2Label.append(line)

    def _load_model(self):
        self.model = load_model(self.MODEL_PATH)
        global graph
        graph = tf.get_default_graph()

    def __init__(self):
        K.clear_session()
        self._set_path()
        self._restore_data()
        self._load_model()

    def _get_stem(self, token):
        stem = self.stem_cache.get(token, None)
        if stem:
            return stem
        token = self.regex.sub('', token).lower()
        stem = self.stemer.stem(token)
        self.stem_cache[token] = stem
        return stem

    def _sentence_to_vector(self, text):
        vector = np.zeros(self.VOCAB_SIZE, dtype=np.int_)
        tokens = text.split()
        for token in tokens:
            stem = self._get_stem(token)
            idx = self.token2Index.get(stem, None)
            if idx is not None:
                vector[idx] = 1
        return vector

    def get(self, sent):
        global graph
        vect = np.array([np.array(self._sentence_to_vector(sent))])
        with graph.as_default():
            data = self.model.predict(vect)[0]
        maxim = 0
        index = 0
        for ind, zn in enumerate(data):
            if zn > maxim:
                index = ind
                maxim = zn
        return self.index2Label[index]
