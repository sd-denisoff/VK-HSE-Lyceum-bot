import numpy as np
import pandas as pd

import re
import tensorflow as tf

from collections import Counter
from sklearn.model_selection import train_test_split
from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import TweetTokenizer

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Input
from keras.preprocessing.text import Tokenizer
from keras.models import load_model

class findClass:
    latent_dim = 380
    data_path = 'textParsing/data/class_data.txt'
    model_path = 'textParsing/models/class_data.h5'
    max_decoder_seq_length = 0

    input_texts = []
    target_texts = []
    input_characters = set()
    target_characters = set()
    num_encoder_tokens = 0
    num_decoder_tokens = 0
    max_encoder_seq_length = 0
    max_decoder_seq_length = 0
    input_token_index = {}
    target_token_index = {}

    encoder_model = 0
    decoder_model = 0

    previosText = ""

    def delSign(self, s):
        delitable_sign = set('.?!')
        for i in delitable_sign:
            s = s.replace(i, '')
        return s


    def prepearing_data(self):
        self.input_characters = sorted(list(self.input_characters))
        self.target_characters = sorted(list(self.target_characters))
        self.num_encoder_tokens = len(self.input_characters)
        self.num_decoder_tokens = len(self.target_characters)
        self.max_encoder_seq_length = max([len(txt) for txt in self.input_texts])
        self.max_decoder_seq_length = max([len(txt) for txt in self.target_texts])

        self.input_token_index = dict(
            [(char, i) for i, char in enumerate(self.input_characters)])
        self.target_token_index = dict(
            [(char, i) for i, char in enumerate(self.target_characters)])

        self.encoder_input_data = np.zeros(
            (len(self.input_texts), self.max_encoder_seq_length,  self.num_encoder_tokens),
            dtype='float32')

        for i, input_text in enumerate(self.input_texts):
            for t, char in enumerate(input_text):
                self.encoder_input_data[i, t, self.input_token_index[char]] = 1.

    def prepearing_model(self):
        self.model = load_model(self.model_path)

        encoder_inputs = self.model.input[0]
        encoder_outputs, state_h_enc, state_c_enc = self.model.layers[2].output
        encoder_states = [state_h_enc, state_c_enc]
        self.encoder_model = Model(encoder_inputs, encoder_states)

        self.encoder_model._make_predict_function()

        decoder_inputs = self.model.input[1]
        decoder_state_input_h = Input(shape=(self.latent_dim,), name='input_3')
        decoder_state_input_c = Input(shape=(self.latent_dim,), name='input_4')
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_lstm = self.model.layers[3]
        decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
            decoder_inputs, initial_state=decoder_states_inputs)
        decoder_states = [state_h_dec, state_c_dec]
        decoder_dense = self.model.layers[4]
        decoder_outputs = decoder_dense(decoder_outputs)
        self.decoder_model = Model(
            [decoder_inputs] + decoder_states_inputs,
            [decoder_outputs] + decoder_states)

        self.decoder_model._make_predict_function()

        self.reverse_input_char_index = dict(
            (i, char) for char, i in self.input_token_index.items())
        self.reverse_target_char_index = dict(
            (i, char) for char, i in self.target_token_index.items())


    def decode_sequence(self, input_seq):
        states_value = self.encoder_model.predict(input_seq)

        target_seq = np.zeros((1, 1, self.num_decoder_tokens))
        stop_condition = False
        decoded_sentence = ''
        while not stop_condition:
            output_tokens, h, c = self.decoder_model.predict(
                [target_seq] + states_value)

            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_char = self.reverse_target_char_index[sampled_token_index]
            decoded_sentence += sampled_char

            if (sampled_char == '\n' or
               len(decoded_sentence) > self.max_decoder_seq_length):
               stop_condition = True

            target_seq = np.zeros((1, 1, self.num_decoder_tokens))
            target_seq[0, 0, sampled_token_index] = 1.

            states_value = [h, c]

        return decoded_sentence

    def read_data(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for line in lines[: len(lines) - 1]:
            line = line.lower()

            line = line.split(';')

            input_text = self.delSign(line[0])
            target_text = '\t' + line[1] + '\n'

            self.input_texts.append(input_text)
            self.target_texts.append(target_text)

            previosText = line

            for char in input_text:
                if char not in self.input_characters:
                    self.input_characters.add(char)

            for char in target_text:
                if char not in self.target_characters:
                    self.target_characters.add(char)

    def __init__(self):
        self.read_data()
        self.prepearing_data()
        self.prepearing_model()


    def deleteUnkownLetters(self, input_text):
        result = ""
        for letter in input_text:
            if (letter in self.input_characters):
                result += letter

        return result

    def get(self, s):
        s = s.lower()
        s = self.deleteUnkownLetters(self.delSign(s))
        input_seq = np.zeros((1, self.max_encoder_seq_length, self.num_encoder_tokens), dtype='float32')
        for t, char in enumerate(s):
            input_seq[0, t, self.input_token_index[char]] = 1.

        decoded_sentence = self.decode_sequence(input_seq)
        return decoded_sentence
