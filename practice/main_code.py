from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from time import time
import random
import string


def preprocessData():
    with open('movie_rev.txt', 'r') as f:
        text_list = f.readlines()
    positive_list = []
    negative_list = []
    positive_result = []
    negative_result = []
    for each in text_list:
        each = each.translate(string.maketrans("", ""), string.punctuation)
        each = each.replace('\t', "").replace('\n', '')
        if each[-1] == '1':
            positive_list.append(each[:-1])
            positive_result.append('1')
        else:
            negative_list.append(each[:-1])
            negative_result.append('0')
    random.shuffle(positive_list)
    random.shuffle(negative_list)
    features_train = positive_list[0:400] + negative_list[0:400]
    features_test = positive_list[400:] + negative_list[400:]
    labels_train = positive_result[0:400] + negative_result[0:400]
    labels_test = positive_result[400:] + negative_result[400:]
    # vectorizer
    vectorizer = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 7), stop_words='english', max_df=0.8)
    features_train_transformed = vectorizer.fit_transform(features_train).toarray()
    features_test_transformed = vectorizer.transform(features_test).toarray()
    return features_train_transformed, features_test_transformed, labels_train, labels_test


def main():
    features_train, features_test, labels_train, labels_test = preprocessData()
    clf = MultinomialNB()
    # fit/train
    t0 = time()
    clf.fit(features_train, labels_train)
    print "training time:", round(time() - t0, 3), "s"
    # predict
    t0 = time()
    pred = clf.predict(features_test)

    print "predicting time:", round(time() - t0, 3), "s"  # accuracy
    accuracy = accuracy_score(labels_test, pred)
    print accuracy


if __name__ == "__main__":
    main()
