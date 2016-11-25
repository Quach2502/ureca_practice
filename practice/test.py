import nltk
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
import string
import networkx as nx
from nltk.stem.wordnet import WordNetLemmatizer
import matplotlib.pyplot as plt
from xml.etree import ElementTree as ET

# from nltk.stem.snowball import SnowballStemmer
dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

def ParseContext(sentence, aspect_term, from_char, to_char):
    from_index, to_index = PositionOfAspectTerm(sentence, aspect_term, from_char, to_char)
    source_fromIndex = str(from_index + 1)
    source_toIndex = str(to_index + 1)
    parse_sent = dep_parser.raw_parse(sentence)
    dep = parse_sent.next()
    G = nx.Graph()
    context = []
    for each in dep.to_dot().split("\n")[4:-1]:  # Use index [4:-1] to get the text only
        # Convert the input from unicode to text
        each = str(each)
        # Remove all the punctuations except ">","=" to identify the relationship in the graph
        each = each.translate(string.maketrans("", ""), string.punctuation.replace(">", "").replace("=", ""))
        # If there is ">" the text is about the relationship( edge)
        if ">" in each:
            relationship = each.split("=")[-1]
            each = each.split()
            G.add_edge(each[0], each[2], label=relationship)
        else:
            each = each.split()
            G.add_node(each[0], name=each[-1])
    name_attribute = nx.get_node_attributes(G, 'name')
    parse_context_fromIndex = nx.single_source_shortest_path_length(G, source_fromIndex, cutoff=3)
    for each in parse_context_fromIndex.keys():
        condition = int(each)
        if (condition > 0 and (condition <= (from_index+1) or condition >= (to_index+1))):
            context.append(name_attribute[each])
    if (to_index != from_index):
        parse_context_toIndex = nx.single_source_shortest_path_length(G, source_toIndex, cutoff=3)
        for each in parse_context_toIndex.keys():
            condition = int(each)
            if (condition > 0 and (condition < (from_index + 1) or condition > (to_index + 1))):
                context.append(name_attribute[each])
    return list(set(context))  # Return the nodes (words) in the parse tree that are connected to the aspect term by at most three edges
def ParseFeatures(sentence, aspect_term, from_char, to_char):
    parseContext = ParseContext(sentence, aspect_term, from_char, to_char)
    # dict_postag = {'word1':'POSTAG1','word2':'POSTAG2'}
    result = []
    dict_postag = {}
    postag = nltk.pos_tag(nltk.word_tokenize(sentence))
    # Create a dictionary with words as keys and POS_TAG as values
    for each in postag:
        dict_postag[each[0]] = each[1]
    for each in parseContext:
        result.append(each + '_' + dict_postag[each])  # Word_POSTAG in the parse context
    slice = sentence.partition(aspect_term)
    for word in parseContext:
        # Determine whether the word is before or after the aspect term to form the correct bigrams context target
        if word in slice[0]:
            result.append(word + "_" + aspect_term + "_ct")
        elif word in slice[2]:
            result.append(aspect_term + "_" + word + "_ct")
    return result
def PositionOfAspectTerm(sentence, aspect_term, from_char,
                         to_char):  # Return the position of aspect term in a given sentence with given from/to positions of character
    list_sentence = sentence.split()
    from_index = 0
    to_index = 0
    position = 0
    # from_index and to_index is the position of the aspect term in the list
    for each in list_sentence:
        if (position + len(each) + 1) <= int(from_char):
            position += len(each) + 1
        else:
            from_index = list_sentence.index(each)
            break
    position = 0
    # if the aspect term is only 1 word so from_index = to_index
    if len(aspect_term.split()) == 1:
        to_index = from_index
    else:
        for each in list_sentence:
            if position + len(each) + 1 < int(to_char):
                position += len(each) + 1
            else:
                to_index = list_sentence.index(each)
                break
    return from_index, to_index


# path_to_jar = 'D:\stanford-parser-full-2015-12-09\stanford-parser-full-2015-12-09\stanford-parser.jar'
# path_to_models_jar = 'D:\stanford-parser-full-2015-12-09\stanford-parser-full-2015-12-09\stanford-parser-3.6.0-models.jar'
def SentenceTransform(sentence, aspect_term, from_char, to_char, window_size):
    parse_feats = ParseFeatures(sentence, aspect_term, from_char, to_char)
    return ' '.join(parse_feats)


def PreprocessData():
    text = []
    tree = ET.parse('restaurants-trial.xml')
    root = tree.getroot()
    for sentence in root.findall('sentence'):
        if sentence.find('aspectTerms') is None:
            continue
        content = sentence.find('text').text.translate(string.maketrans("", ""), string.punctuation)
        for aspectTerms in sentence.iter('aspectTerms'):
            for aspectTerm in aspectTerms.iter('aspectTerm'):
                text.append(SentenceTransform(content, aspectTerm.get('term').translate(string.maketrans("", ""),
                                                                                        string.punctuation),
                                              aspectTerm.get("from"), aspectTerm.get("to"), 10))
    return text
def main():
    print len(PreprocessData())
if __name__ == "__main__":
    main()

# sentence = "The decor is vibrant and eye-pleasing with several semi-private boths on the right side of the dining hall, which are great for a date"
# aspect_term = "decor"
# from_index = 1
# to_index = 1
# list_word = nltk.word_tokenize(sentence)
# postag = nltk.pos_tag(list_word)
# dict_postag = {}
# for each in postag:
#     dict_postag[each[0]] = each[1]
# result = dep_parser.raw_parse(sentence)
# dep = result.next()
# G = nx.Graph()
# # a = list(dep.triples())
# # for triple in dep.triples():
# #     print triple[1],"(",triple[0][0],", ",triple[2][0],")"
# # for each in dep.to_dot().split("\n")[4:-1]:
# #     each = str(each)
# #     each = each.translate(string.maketrans("", ""), string.punctuation.replace(">", "").replace("=", ""))
# #     if ">" not in each:
# #         each = each.split()
# #         label_node[each[0]] = each[-1]
# for each in dep.to_dot().split("\n")[4:-1]:
#     each = str(each)
#     each = each.translate(string.maketrans("", ""), string.punctuation.replace(">", "").replace("=", ""))
#     if ">" in each:
#         relationship = each.split("=")[-1]
#         each = each.split()
#         G.add_edge(each[0], each[2], label = relationship)
#     else:
#         each = each.split()
#         G.add_node(each[0], name = each[-1])
# name_attribute = nx.get_node_attributes(G,'name')
# source_fromIndex = str(from_index +1)
# target_toIndex = str(to_index+1)
# parse_context_length = nx.single_source_shortest_path_length(G,source_fromIndex,cutoff = 3)
# for each in parse_context_length.keys():
#     if each != source_fromIndex:
#         for path in nx.all_simple_paths(G, source=source_fromIndex, target=each):
#             for element in path:
#                 print name_attribute[element]+'_',
#             print
# for each in G.nodes():
#      print
# nx.draw_networkx_edge_labels(DG,pos,edge_labels=edge_labels)
# nx.draw_networkx(DG, pos, labels=node_labels)
# plt.show()
# aspect_Term = "dining hall"
# test = test.split()
# position = 0
# from_index =0
# to_index = 0
# to_char = 106
# from_char = 95
# for each in test:
#     print each, len(each)
#     if position + len(each) + 1 <= from_char:
#         position += len(each) + 1
#     else:
#         from_index = test.index(each)
#         break
# position = 0
# if len(aspect_Term.split()) == 1:
#     to_index = from_index
# else:
#     for each in test:
#         if position + len(each) + 1 < to_char:
#             position += len(each) + 1
#         else:
#             to_index =test.index(each)
#             break
# print from_index, to_index

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

# grammar = r"""
#         NP:     {<PDT>?<DT|IN|WDT|WP\$|PRP\$>?<CD|JJ.*>*<PRP|WP|NN.*>+}
#         PP:     {<IN|TO|RP><NP>}
#         VP:     {<RB.?>*<MD>*<TO>*<VB.?>+<RB.*|WRB>*<RP>*<NP|PP|JJ*>*}
#         CL:     {<NP><VP>}
#          """
# grammar = r"""
#     NP:
#         {<NN><NN><NN>}
#         {<NNP><NNP><NNP>}
#         {<NNP><NNP><NN>}
#         {<NNS><NN><NN>}
#         {<FW><NN><NN>}
#         {<NN><NN>}
#         {<NNP><NNP>}
#         {<NNP><NN>}
#         {<FW><NN>}
#         {<NNS><NNS>}
#         {<NN><NNS>}
#         {<DT><JJ><NNS>}
#         {<IN><JJ><NNS>}
#         {<NN>}
#         {<NNP>}
#         {<NNS>}
#         {<DT>?<JJ>*<NN>}
#      """
# print postagger
# parser = nltk.RegexpParser(grammar)
# result = parser.parse(postagger)
# print result
# result.draw()
