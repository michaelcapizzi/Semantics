__author__ = 'mcapizzi'

from gensim import models
from gensim import corpora
import itertools
import nltk


class Embedding:
"""Generates the word2vec vectors to be used:
    (1) use GoogleNews vectors
    (2) build directly from wikipedia dump using corpus methods
    (3) manually build
"""


    def __init__(self, filePath="/home/mcapizzi/Google_Drive_Arizona/Programming/word2Vec/GoogleNews-vectors-negative300.bin.gz"):
        self.W2Vpath = filePath
        self.embeddingModel = None
        self.trainingSentences = []
        self.total_words = len(list(itertools.chain(*self.trainingSentences)))
        self.corpus = 0

####
#use GoogleNews vectors
####
    def useDefault(self):
        self.embeddingModel = models.Word2Vec.load_word2vec_format(fname=self.W2Vpath, binary=True, norm_only=True)

####
#use built in wiki corpus
####

    #builds initial corpus from Wikipedia dump file
    def buildCorpus(self, fname):
        self.corpus = corpora.WikiCorpus(fname)

    #train directly from wikipedia corpus
    def trainFromCorpus(self, window, min_count, workers, negative, size=100):
        self.embeddingModel = models.word2vec.Word2Vec(sentences=self.trainingSentences, size=size, window=window, min_count=min_count, workers=workers, negative=negative)
        inputText = self.corpus.get_texts()
        #TODO add preprocessing (lowercase, lemmatize?)
        self.embeddingModel.build_vocab(self.corpus.get_texts())
        self.embeddingModel.train(self.corpus.get_texts())

####
#train new vectors
####

    #add tokenized sentences to be used
    def addTrainingSentences(self, listOfSentences):
        self.trainingSentences = listOfSentences


    #build a model with pre-loaded sentences
    def buildModel(self, window, min_count, workers, negative, size=100):
        self.embeddingModel = models.word2vec.Word2Vec(sentences=self.trainingSentences, size=size, window=window, min_count=min_count, workers=workers, negative=negative)
        #when all training is complete - saves memory
        self.embeddingModel.init_sims(replace=True)


    #train line by line in stream
    def trainLineByLine(self, stream, window, min_count, workers, negative, size=100):
        #intialize model
        self.embeddingModel = models.word2vec.Word2Vec(sentences=None, size=size, window=window, min_count=min_count, workers=workers, negative=negative)

        #add sentences to vocabulary and train
        for line in stream:
            #decode in utf8
            decoded = line.decode("utf8")
            #sentence tokenize
            sentences = nltk.sent_tokenize(decoded)
            #word tokenize
            tokenizedSentences = [nltk.word_tokenize(s) for s in sentences]
            #add to vocabulary
            self.embeddingModel.build_vocab(tokenizedSentences)
            #update model
            self.embeddingModel.train(tokenizedSentences)


####
#miscellaneous
####

    #when all training is complete
    def endTraining(self):
        self.embeddingModel.init_sims(replace=True)


    #save model to disk
    def saveModel(self, fname):
        self.embeddingModel.save(fname)


    #load model from file
    def loadModel(self, fname):
        self.embeddingModel.load(fname)
