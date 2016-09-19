#from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize
from time import time
import nltk
import random
import string

stemmer = SnowballStemmer('english')
list_stopword = [var for var in stopwords.words('english') if var not in ['not','isn']]


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def preprocessData():
    with open('movie_rev.txt', 'r') as f:
        text_list = f.readlines()
    positive_list = []
    negative_list = []
    positive_result = []
    negative_result = []
    for each in text_list:
        each = each.translate(string.maketrans("", ""), string.punctuation)
        each = each.replace('\t', "").replace('\n', '').lower().strip()
        if each[-1] == '1':
            positive_list.append(each[:-1].strip())
            positive_result.append('1')
        else:
            negative_list.append(each[:-1].strip())
            negative_result.append('0')
    random.shuffle(positive_list)
    random.shuffle(negative_list)
    features_train = positive_list[0:400] + negative_list[0:400]
    features_test = positive_list[400:] + negative_list[400:]
    labels_train = positive_result[0:400] + negative_result[0:400]
    labels_test = positive_result[400:] + negative_result[400:]
    # vectorizer
    vectorizer = TfidfVectorizer(tokenizer=tokenize, sublinear_tf=True, ngram_range=(1, 6),
                                 stop_words=list_stopword,
                                 max_df=0.8)
    features_train_transformed = vectorizer.fit_transform(features_train).toarray()
    features_test_transformed = vectorizer.transform(features_test).toarray()
    return features_test,features_train_transformed, features_test_transformed, labels_train, labels_test, vectorizer


def main():
    original_features_test,features_train, features_test, labels_train, labels_test, vectorizer = preprocessData()
    clf = RadiusNeighborsClassifier(weights='distance',algorithm='brute',radius=2)
    # fit/train
    t0 = time()
    clf.fit(features_train, labels_train)
    print "training time:", round(time() - t0, 3), "s"
    # predict
    t0 = time()
    pred = clf.predict(features_test)
    print "predicting time:", round(time() - t0, 3), "s"  # accuracy
    print metrics.accuracy_score(labels_test, pred)
    print clf.predict(vectorizer.transform(['awesome']).toarray()) #for testing specific string
    for i in range(1,len(pred)):  #print out all false result
        if labels_test[i] != pred[i]:
            print original_features_test[i] + '\t' + pred[i]
    print metrics.confusion_matrix(labels_test,pred)

if __name__ == "__main__":
    main()
