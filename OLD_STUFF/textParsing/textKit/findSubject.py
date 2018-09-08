import pandas as pd
import numpy as np
import re

from nltk.stem.snowball import RussianStemmer

class findSubject:
    SUBJECTS_NAME = []
    SUBJECTS_REAL_NAME = []
    IS_LOADED_SUBJECTS = False

    regex = 0
    stemer = 0

    def __init__(self):
        self.stemer = RussianStemmer()
        self.regex = re.compile('[^а-яА-Я ]')
        self.load_subjects('textParsing/data/subjects.csv')

    def get_stem(self, token, checkHash = True):
        token = self.regex.sub('', token).lower()
        stem = self.stemer.stem(token)
        return stem

    def load_subjects(self, filepath):
        pd_subjects = pd.read_csv(filepath, delimiter = ';')
        self.SUBJECTS_NAME = list(np.array(pd_subjects[['name']]))
        self.SUBJECTS_REAL_NAME = list(np.array(pd_subjects[['subject']]))

        for ind in range(len(self.SUBJECTS_NAME)):
            self.SUBJECTS_NAME[ind] = self.get_stem(str(self.SUBJECTS_NAME[ind][0]), False)

        self.IS_LOADED_SUBJECTS = True

    def get(self, text):

        sent = text.split(' ');
        find_fst_po = -1

        for ind, word in enumerate(sent):
            if word == 'по':
                find_fst_po = ind
                break
        if (find_fst_po == -1):
            return None

        subjects = set()

        for ind, word in enumerate(sent):
            if (ind > find_fst_po):
                word = self.get_stem(word, False)
                if (word in self.SUBJECTS_NAME):
                    subjects.add(str(self.SUBJECTS_REAL_NAME[self.SUBJECTS_NAME.index(word)]))

        if (len(subjects) == 0):
            return None

        return subjects
