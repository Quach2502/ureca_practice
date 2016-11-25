# from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize
from time import time
from copy import deepcopy
from scipy.sparse import csr_matrix
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import random
import string

stemmer = SnowballStemmer('english')
list_stopword = [var for var in stopwords.words('english') if var not in ['not', 'isn']]


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def GetXYVocab(NumpSamples=-1):
    Lines = [l.strip() for l in open('movie_rev.txt').xreadlines()]
    Samples, Y = [], []
    for each in Lines:
        each = each.translate(string.maketrans("", ""), string.punctuation)
        each = each.replace('\t', "").replace('\n', '').lower().strip()
        Samples.append(each[:-1].strip())
        if each[-1] == '1':
            Y.append('1')
        if each[-1] == '0':
            Y.append('0')
        if each[-1] == '2':
            Y.append('2')

    CountVecter = CountVectorizer(lowercase=False, dtype=np.float64, binary=False)  # ,max_df=0.95)
    X = CountVecter.fit_transform(Samples)
    X = Normalizer().fit_transform(X)
    print 'shape of X matrixs', X.shape
    Vocab = CountVecter.get_feature_names() + ['HLPos', 'HLNeg', 'HLSum', 'NrcPos', 'NrcNeg', 'NrcSum', 'SubjPos',
                                               'SubjNeg', 'SubjSum']
    return X, Y, Vocab


    # def preprocessData():
#     with open('movie_rev.txt', 'r') as f:
#         text_list = f.readlines()
#     positive_list = []
#     negative_list = []
#     positive_result = []
#     negative_result = []
#     for each in text_list:
#         each = each.translate(string.maketrans("", ""), string.punctuation)
#         each = each.replace('\t', "").replace('\n', '').lower().strip()
#         if each[-1] == '1':
#             positive_list.append(each[:-1].strip())
#             positive_result.append('1')
#         else:
#             negative_list.append(each[:-1].strip())
#             negative_result.append('0')
#     random.shuffle(positive_list)
#     random.shuffle(negative_list)
#     features_train = positive_list[0:400] + negative_list[0:400]
#     features_test = positive_list[400:] + negative_list[400:]
#     labels_train = positive_result[0:400] + negative_result[0:400]
#     labels_test = positive_result[400:] + negative_result[400:]
#     # vectorizer
#     vectorizer = TfidfVectorizer(tokenizer=tokenize, sublinear_tf=True, ngram_range=(1, 3),
#                                  stop_words=list_stopword,
#                                  max_df=0.8)
#     features_train_transformed = vectorizer.fit_transform(features_train).toarray()
#     features_test_transformed = vectorizer.transform(features_test).toarray()
#     # CountVecter = CountVectorizer(lowercase=False, dtype=np.float64, binary=False)  # ,max_df=0.95)
#     # X = CountVecter.fit_transform(features_train)
#     # X = Normalizer().fit_transform(X)
#     # Vocab = CountVecter.get_feature_names()
#     # Y = labels_train
#     return features_train, features_test, features_train_transformed, features_test_transformed, labels_train, labels_test, vectorizer, Vocab


def GetTopN(W, Vocab, N=20):
    FeatsAndVocab = zip(W.tolist(), Vocab)
    FeatsAndVocab.sort()
    FeatsAndVocab.reverse()
    return FeatsAndVocab[:N]


def AnalyseClassifierFeats(Classifier, Vocab, TopN=20):
    W = deepcopy(Classifier.coef_)
    NegW = W[0, :]
    NeuW = W[1, :]
    PosW = W[2, :]

    TopNeg = GetTopN(NegW, Vocab, TopN)
    TopNeu = GetTopN(NeuW, Vocab, TopN)
    TopPos = GetTopN(PosW, Vocab, TopN)
    # TopConf =  GetTopN(ConfW, Vocab, TopN)
    # return TopNeg, TopNeu, TopPos, TopConf
    return TopNeg, TopNeu,TopPos


def main():
    # original_features_train, original_features_test, features_train, features_test, labels_train, labels_test, vectorizer, Vocab = preprocessData()
    X, Y, Vocab = GetXYVocab(-1)
    # clf = RadiusNeighborsClassifier(weights='distance', algorithm='brute', radius=2)
    clf = LinearSVC(C=0.01)
    # fit/train
    # t0 = time()
    # clf.fit(features_train, labels_train)
    # print "training time:", round(time() - t0, 3), "s"
    # # predict
    # t0 = time()
    # pred = clf.predict(features_test)
    # print "predicting time:", round(time() - t0, 3), "s"  # accuracy
    # print metrics.accuracy_score(labels_test, pred)
    clf.fit(X, Y)

    X = csr_matrix(X)
    TopN = 20
    # TopNeg, TopNeu, TopPos, TopConf = AnalyseClassifierFeats (Classifier, Vocab, TopN)
    TopNeg, TopNeu, TopPos = AnalyseClassifierFeats(clf, Vocab, TopN)
    print '*' * 80
    print 'top {} pos feats: '.format(TopN);
    pprint(TopPos);
    print '*' * 80
    print 'top {} neg feats: '.format(TopN);
    pprint(TopNeg);
    print '*' * 80
    print 'top {} neu feats: '.format(TopN);
    pprint(TopNeu);
    print '*' * 80

    # print clf.predict(vectorizer.transform(['awesome', 'not bad']).toarray())  # for testing specific string

    # for i in range(1, len(pred)):  # print out all false result
    #     if labels_test[i] != pred[i]:
    #         print original_features_test[i] + '\t' + pred[i]
    # print metrics.confusion_matrix(labels_test, pred)
    # features_train_tokens = vectorizer.get_feature_names()
    # positive_count = clf.feature_count_[1, :]
    # negative_count = clf.feature_count_[0, :]
    # tokens = pd.DataFrame({'token': features_train_tokens, 'positive': positive_count, 'negative': negative_count})
    # tokens['negative_ratio'] = (tokens.negative+1) / (tokens.positive+1)
    # print tokens.sort_values('negative_ratio',ascending=False)


if __name__ == "__main__":
    main()
