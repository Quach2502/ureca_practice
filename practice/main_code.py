from nltk.stem.snowball import SnowballStemmer
from sklearn.naive_bayes import GaussianNB
import string

def preprocessData():
    with open('movie_rev.txt', 'r') as f:
        text_list = f.readlines()
    output  = []
    for each in text_list:
        each = each.translate(string.maketrans("",""),string.punctuation)
        each = each.replace('\t', " ").replace('\n', " ").replace('\r', " ")
        output.append(each)
    return output


def main():
    data = preprocessData()
    for var in data:
        print var


if __name__ == "__main__":
    main()
