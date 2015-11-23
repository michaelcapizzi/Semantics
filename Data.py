from nltk.parse.stanford import StanfordParser

__author__ = 'mcapizzi'

import re
import nltk as nl

class Data:

    def __init__(self, file):
        self.file = file
        self.allSentences = []

    #sentence tokenize incoming lines
    def sentenceTokenize(self):
        for line in self.file:
            #decode in utf8
            decoded = line.decode("utf8")
            #sentence tokenize
            tokenizedSentences = nl.sent_tokenize(decoded)
            #flatten and add to allSentences
            [self.allSentences.append(i.rstrip()) for i in tokenizedSentences]

    #removes \n and <doc and titles
    def cleanAllSentences(self):
        newLine = "\n"
        docRegex = "<doc"
        titleRegex = r'^\w+'
        self.allSentences = filter(lambda x:    x != newLine or
                                                x.startswith(docRegex) == False or
                                                x.#TODO add titleRegex
                                                            self.allSentences)


#for line in f:
    #decoded = line.decode("utf8")
    #nltk.sent_tokenize(decoded.rstrip())

