__author__ = 'Arpana'

import nltk
from nltk.tag.simplify import simplify_wsj_tag
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import *


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
            stem_word = stem_word + " " +stemmer.stem(wrd[0])
        print "#######STEMMING#######"
        print stem_word
        """
        LEMMATIZING
        """
        print tagged_sent
        lmtzr = WordNetLemmatizer()
        sent = ""
        for wrd in tagged_sent:

            sent = sent + " " +lmtzr.lemmatize(wrd[0])
        print "#######LEMMA"""""""
        print sent

        #left_line = line[:split_at].split()
        #left = line [:split_at]
        #right = line [:split_at+1]
        #print "starting"
        #print left
        #print right
        # break


def main():
    file_object = open('train.data','r')
    read_file(file_object)

main()