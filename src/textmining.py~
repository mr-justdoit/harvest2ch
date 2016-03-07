# coding: utf-8
from __future__ import absolute_import, print_function
from janome.tokenizer import Tokenizer
from itertools import groupby
from nltk.tokenize import TweetTokenizer
import sys
import re
import nltk
import pyaml


def filter(text):
    text = re.sub(r'[a-zA-Z0-9¥"¥.¥,¥@]+', '', text)
    text = re.sub(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]', '', text)
    text = re.sub(r'[\n|\r|\t]', '', text)

    jp_chartype_tokenizer = nltk.RegexpTokenizer(
        u'([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\u9FFF]+|[ぁ-んァ-ンー\u4e00-\u9FFF]+)')
    text = "".join(jp_chartype_tokenizer.tokenize(text))
    return text


def text_to_array(textdata):
    t = TweetTokenizer()
    textdata = sorted(t.tokenize(textdata))
    return textdata


def count_words(words):
    keys = [key for key, group in groupby(words)]
    values = [len(list(group)) for key, group in groupby(words)]
    return dict(zip(keys, values))


def output_ja_text(data, wordtypes):
    textdata = filter(data)
    t = Tokenizer()
    tokens = t.tokenize(textdata)
    words = sorted([token.surface
                    for token in tokens
                    if token.part_of_speech.split(',')[0] in wordtypes])
    dictionary = count_words(words)
    return pyaml.dump(dictionary, sys.stdout, vspacing=[0, 1])


def output_textdata(data):
    textdata = data
    words = text_to_array(textdata)
    dictionary = count_words(words)
    return pyaml.dump(dictionary, sys.stdout, vspacing=[0, 1])
