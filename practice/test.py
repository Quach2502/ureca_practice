import nltk
from nltk.parse.stanford import StanfordDependencyParser
path_to_jar = 'C:\Users\t_quacd\AppData\Local\stanford-parser-full-2015-12-09/stanford-parser.jar'
path_to_models_jar = 'C:\Users\t_quacd\AppData\Local\stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
sentence = "I  enjoy the service but the food is not good"
test = parser.raw_parse(sentence)
dep = test.next()
print list(dep.triples())
list_word = nltk.word_tokenize(sentence)
postagger = nltk.pos_tag(list_word)
# grammar = r"""
#         NP: {<PDT>?<DT|WDT|WP\$|PRP\$>?<CD|JJ.*>*<PRP|WP|NN.*>+}
#         PP: {<IN|TO|RP><NP>}
#         VP: {<RB|RBS|WRB>*<MD>*<TO>*<VB.*>+<RB.*|WRB>*<RP>*<NP|PP|CL>*$}
#         CL: {<NP><VP>}
#             {<NP><.*>?<VB.*><RB>*<JJ.*>}
#         """
grammar = r"""
    NP: #
        {<NN><NN><NN>}
        {<NNP><NNP><NNP>}
        {<NNP><NNP><NN>}
        {<NNS><NN><NN>}
        {<FW><NN><NN>}
        {<NN><NN>}
        {<NNP><NNP>}
        {<NNP><NN>}
        {<FW><NN>}
        {<NNS><NNS>}
        {<NN><NNS>}
        {<DT><JJ><NNS>}
        {<IN><JJ><NNS>}
        {<NN>}
        {<NNP>}
        {<NNS>}
     """
print postagger
parser = nltk.RegexpParser(grammar)
result = parser.parse(postagger)
print result
result.draw()
