__author__ = 'Arpana'

import nltk
import string
import itertools
import re
from nltk.tag.simplify import simplify_wsj_tag
from nltk.tokenize.punkt import PunktWordTokenizer
from collections import defaultdict, namedtuple
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import *


class WordFeatureMap(object):
    def __init__(self, sense=1, feature_vectors_prob=None, prob_sense=0):
        if feature_vectors_prob is None:
            self.feature_vectors_prob = {}
        else:
            self.feature_vectors_prob = feature_vectors_prob
        self.sense = sense
        self.prob_sense = prob_sense


def process_word_context(entire_context):
    #remove punct
    cont_without_punct = entire_context.translate(string.maketrans('', ''), r'!"#$&\'()*+,-./:;<=>?@[\\]^_`{}~')
    cont_without_punct = " ".join(cont_without_punct.split())
    #pos tagging
    tagged_sent = [(word, simplify_wsj_tag(tag)) for word, tag in nltk.pos_tag(cont_without_punct.split(" "))]

    #stop words removal
    stopwords = nltk.corpus.stopwords.words('english')
    pos_tag_without_stopwords = [wrd for wrd in tagged_sent if wrd[0].lower() not in stopwords]

    for i, pos_tag_tuple in enumerate(pos_tag_without_stopwords):
        if pos_tag_tuple[0] == '%%':
            prev_context, target_word, next_context = pos_tag_without_stopwords[:i], pos_tag_without_stopwords[i + 1], \
                                                      pos_tag_without_stopwords[i + 3:]
            break

    return prev_context, next_context


def select_window_feature(context, direction, feature_window=5):
    context = reversed(context) if direction == -1 else context
    feature_vector = []
    fea_cnt = 0
    for p_fea in context:
        if fea_cnt >= feature_window:
            break
        if p_fea[1] in ['N', 'ADJ', 'V', 'ADV']:
            feature_vector.append(p_fea)
            fea_cnt += 1

    return feature_vector


word_feature_dict = {}
word_sense_count = defaultdict(int)
word_total_count = defaultdict(int)
feature_count = defaultdict(int)


def do_something():
    WordSense = namedtuple("WordSense", ['word', 'sense'])
    with open('train.data') as f:
        for line in f:
            components = line.split("|")
            #target_word = components[0].split(".")
            target_word = components[0]
            sense = components[1]
            wordsense = WordSense(target_word, sense)

            prev_context, next_context = process_word_context(components[2])
            feature_vector_list = itertools.chain(select_window_feature(prev_context, -1),
                                                  select_window_feature(next_context, 1))

            word_sense_count[wordsense] += 1
            word_total_count[target_word] += 1

            for fv in feature_vector_list:
                feature_count[(fv, wordsense)] += 1

        for key, value in word_sense_count.items():
            print "probability of " + key.word + " " + key.sense + " is = " + str(
                float(value) / float(word_total_count[key[0]]))

        for key, value in feature_count.items():
            print "feature vector prob of " + key[0][0] + " wrt " + key[1].word + " " + key[1].sense + " is = " + str(
                value / float(word_sense_count[key[1]]))


def read_file(file_object):
    lines = file_object.readlines()
    for line in lines:
        print "#######LINE#######"
        print line

        text = PunktWordTokenizer().tokenize(line)
        #text = nltk.wordpunct_tokenize(line)
        print "#######TEXT#######"
        print text

        """
        STOP WORD
        """
        stopwords = nltk.corpus.stopwords.words('english')
        content = [w for w in text if w[0].lower() not in stopwords]
        print "#######STOP WORD#######"
        print content

        """
        POS TAGGING
        """
        tagged_sent = nltk.pos_tag(content)
        tagged_sent = [(word, simplify_wsj_tag(tag)) for word, tag in tagged_sent]
        print "#######POS#######"
        print tagged_sent

        """
        STEMMING
        """
        #tagged_sent = tuple(tagged_sent)
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        stem_word = ""
        for wrd in tagged_sent:
            stem_word = stem_word + " " + stemmer.stem(wrd[0])
        print "#######STEMMING#######"
        print stem_word
        """
        LEMMATIZING
        """
        print tagged_sent
        lmtzr = WordNetLemmatizer()
        sent = ""
        for wrd in tagged_sent:
            sent = sent + " " + lmtzr.lemmatize(wrd[0])
        print "#######LEMMA"""""""
        print sent


def main():
    do_something()

#if __name__ == '__main__':
main()