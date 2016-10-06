import nltk

text = nltk.word_tokenize("We are going out just you and me.")
print nltk.pos_tag(text)
