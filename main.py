import nltk
import re
import os
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.parse import stanford
from functools import * 

# !wget 'https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip'
# !unzip 'stanford-tagger-4.2.0.zip'

# jar = '/content/stanford-postagger-4.2.0'
# model = '/content/stanford-postagger-full-2020-11-17/models/english-left3words-distsim.tagger'


# stanford_tagger = StanfordPOSTagger(model, jar, encoding='utf8')


from nltk.tag.stanford import CoreNLPPOSTagger, CoreNLPNERTagger
from nltk.parse.corenlp import CoreNLPParser
stpos, stner = CoreNLPPOSTagger(), CoreNLPNERTagger()
# stpos.tag('What is the airspeed of an unladen swallow ?'.split())

who_query = []
yes_no_query = []
declaration_query = []

#def determine_type(sentence):
# return 

# def declare(declaration):
#   return  
# def yes_no_question(question):
#   return
# def who(question):
#   return

def tokenize(words):
  raw_tokens =  list(filter(lambda x: re.match(r"[A-Za-z]",x),nltk.word_tokenize(words)))
  
  tagged = nltk.pos_tag(raw_tokens) 

  type_map = {'J':wordnet.ADJ,'V':wordnet.VERB,'N':wordnet.NOUN,'R':wordnet.ADV,'D':wordnet.NOUN}
  lemma =  nltk.stem.WordNetLemmatizer()
  return [
      (lemma.lemmatize(token,type_map[type_value[0]]),type_value) if type_value[0] in type_map
      else lemma.lemmatize(token) 
      for token,type_value in tagged
    ]

def create_dict(words):
  type_dict= { wordnet:[] for word, word_type in words }
  for word,word_type in words:
      type_dict[word_type].append(word) 
  return type_dict

def parse(words):
  grammer_str = """
      # % start S
      ############################
      # Grammar rules
      ############################
        S -> NP VP
        PP -> P NP
        NP -> DT N
        N -> N PP
        N -> Adj N
        VP -> IV
        VP -> TV NP
        VP -> DTV NP NP
        VP -> DTV NP PP
        VP -> VP PP
        VP -> SV S
        VP -> AUX VP
        VP -> ADV VP  
        NP -> PN
        NP -> PRN
      ############################ 
"""
  wordtype_dict = create_dict(words)
  
  pls= lambda ls: reduce(lambda type_value,string: string+" "+type_value+"\n" ,ls,"")  

  pk = lambda str_value:str_value+" ->"

  rules= [  pk(k) + pls(ls)  for k,ls in wordtype_dict.items()]
  
  

  my_grammar = nltk.CFG.fromstring(string)
 
  


tokenize("A man entered the dealership.")
determine_type("A man entered the dealership."
