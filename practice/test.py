import nltk
from nltk.corpus import sentiwordnet as swn
sentence = "The food in the restaurant is good but the service is bad"
list_word = nltk.word_tokenize(sentence)
postagger = nltk.pos_tag(list_word)
groucho_grammar =  r"""
        NP: {<PDT>?<DT|WDT|WP\$|PRP\$>?<CD|JJ.*>*<PRP|WP|NN.*>+}
        PP: {<IN|TO|RP><NP>}
        VP: {<RB|RBS|WRB>*<MD>*<TO>*<VB.*>+<RB.*|WRB>*<RP>*<NP|PP|CL>*$}
        CL: {<NP><VP>}
            {<NP><.*>?<VB.*><JJ.*>}
        """
print postagger
parser = nltk.RegexpParser(groucho_grammar)
result = parser.parse(postagger)
print result
result.draw()
