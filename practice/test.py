import nltk
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from xml.etree import ElementTree as ET

tree = ET.parse('restaurants-trial.xml')
root = tree.getroot()
for sentence in root.findall('sentence'):
    print "Sentence:", sentence.find('text').text
    if sentence.find('aspectTerms') is None:
        print "Aspect Term: None"
    else:
        for aspectTerms in sentence.iter('aspectTerms'):
            for aspectTerm in aspectTerms.iter('aspectTerm'):
                print "Aspect Term:", aspectTerm.get('term'), "-", aspectTerm.get("polarity")
# path_to_jar = 'C:\Users\t_quacd\AppData\Local\stanford-parser-full-2015-12-09/stanford-parser.jar'
# path_to_models_jar = 'C:\Users\t_quacd\AppData\Local\stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
# parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
# dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
# sentence = "I enjoy the service but I enjoy the service"
# parsed_Sentence = parser.raw_parse(sentence)
# for line in parsed_Sentence:
#        print line
#        line.draw()
#
# parsed_Sentence = [parse.tree() for parse in dep_parser.raw_parse(sentence)]
# print parsed_Sentence
#
# # GUI
# for line in parsed_Sentence:
#         print line
#         line.draw()
# list_word = nltk.word_tokenize(sentence)
# postagger = nltk.pos_tag(list_word)
# grammar = r"""
#         NP:     {<PDT>?<DT|IN|WDT|WP\$|PRP\$>?<CD|JJ.*>*<PRP|WP|NN.*>+}
#         PP:     {<IN|TO|RP><NP>}
#         VP:     {<RB|RBS|WRB>*<MD>*<TO>*<VB.*>+<RB.*|WRB>*<RP>*<NP|PP|CL>*$}
#                 {<VB.*><RB>*<JJ.*>$}
#         CL:     {<NP><VP>}
#          """
# # grammar = r"""
# #     NP:
# #         {<NN><NN><NN>}
# #         {<NNP><NNP><NNP>}
# #         {<NNP><NNP><NN>}
# #         {<NNS><NN><NN>}
# #         {<FW><NN><NN>}
# #         {<NN><NN>}
# #         {<NNP><NNP>}
# #         {<NNP><NN>}
# #         {<FW><NN>}
# #         {<NNS><NNS>}
# #         {<NN><NNS>}
# #         {<DT><JJ><NNS>}
# #         {<IN><JJ><NNS>}
# #         {<NN>}
# #         {<NNP>}
# #         {<NNS>}
# #         {<DT>?<JJ>*<NN>}
# #      """
# print postagger
# parser = nltk.RegexpParser(grammar)
# result = parser.parse(postagger)
# print result
# result.draw()
