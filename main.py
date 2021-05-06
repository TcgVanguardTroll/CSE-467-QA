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



def tokenize(words):
  raw_tokens =  list(filter(lambda x: re.match(r"[A-Za-z]",x),nltk.word_tokenize(words)))
  
  tagged = nltk.pos_tag(raw_tokens) 
  type_map = {'J':wordnet.ADJ,'V':wordnet.VERB,'N':wordnet.NOUN,'R':wordnet.ADV,'D':wordnet.NOUN}
  lemma =  nltk.stem.WordNetLemmatizer()
  return [
      (lemma.lemmatize(token,type_map[type_value[0]]),type_value) if type_value[0] in type_map
      else (lemma.lemmatize(token),type_value)
      for token,type_value in tagged
    ]


def semantics_interface(tokens):
# take tokens and build a  Semantics interface
    grammer_str = """
    # % start S
    ############################
    # Grammar rules
    ############################
      
      // Declarative
      S[SEM =  <?np(?vp)>]  ->  NP[SEM=?np] VP[SEM=?vp]
      S[SEM =  <?pn(?vp)>]  ->  PN[SEM=?pn] VP[SEM=?vp]
      
      // Wh-Questions
      S[SEM  = <?wp(?vp)>]  ->  WP[SEM=?wp] VP[SEM=?vp]
      
      // Yes-No Questions
      S[SEM  = <?vp(?np)>]  ->  VP[SEM=?vp] NP[SEM=?np]

      NP[SEM = <?dt(?np)>]  ->  DT[SEM=?dt] NP[SEM=?np]
      NP[SEM = <?adj(?np)>] ->  ADJ[SEM=?adj] NP[SEM=?np]
      NP[SEM = <?n(?vp)>]   ->  N[SEM=?n] VP[SEM=?vp]
      NP[SEM = <?pn>]       ->  PN[SEM=?pn]
      NP[SEM = <?n>]        ->  N[SEM=?n]

      
      VP[SEM = <?v(?vp)>]  ->   V[SEM=?v]     VP[SEM=?vp]
      VP[SEM = <?tv(?p)>]   ->  TV[SEM=?tv]   P[SEM=?p]
      VP[SEM = <?itv(?p)>]  ->  ITV[SEM=?itv] P[SEM=?p]
      VP[SEM = <?tv(?p)>]   ->  TV[SEM=?tv]   P[SEM=?p]
      VP[SEM = <?p(?np)>]   ->  P[SEM=?p]     NP[SEM=?np]

      P[SEM = <?dt(?np)>]   -> DT[SEM=?dt] NP[SEM=?np]

    ############################ 
      DT -> A 
      Adj -> tall skinny big strong powerful short huge funny smart nice mean
      P -> about in as to ad into for near above as like since 
      C -> that 
      Aux -> be | have
      WP -> who what 
      ITV -> act adapt crawl danse erupt escape leave start party panic sneeze
      TV -> grab impower hold push build mold hug love juice obliterate 
      N -> man boy cat dog time house company cow program company study owner door check corner job dealership office customer sailor member employee
      PN -> jimmy james jordan grant holtzman bob joe jim jeff george 
  """        
    return grammer_str
    
    
def create_model(v):
      value = nltk.Valuation.fromstring(v)    
      init = nltk.Assignment(value.domain)
      m = nltk.Model(value.domain,value)
      return (m,init) 
    
def verb_checking(verb,noun1,noun2,m,init):
  check_string= f"{verb}({noun1},{noun2})" 
  return m.evaluate(check_string,init) 
    
print(tokenize("what is there?"))
    #determine_type("A man entered the dealership.")
    # part 4
def CFG():
  
  my_grammar = nltk.CFG.fromstring(string)

