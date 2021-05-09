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
      
      // Wh-Questions
      S[SEM  = <?w(?np(?vp))>]             ->  WP[SEM=?w] NP[SEM=?np] VP[SEM=?vp]
      S[SEM  = <?w(?np(?aux(?np(?vp))))>]  ->  WP[SEM=?w] NP[SEM=?np] AUX[SEM=?aux] NP[SEM=?np] VP[SEM=?vp]

      
      // Yes-No Questions
      S[SEM  = <?aux(?np(?vp))>]  ->  AUX[SEM=?aux] NP[SEM=?np] VP[SEM=?vp]

      NP[SEM = <?pn>]        ->  PN[SEM=?pn]
      NP[SEM = <?n>]         ->  N[SEM=?n]
      NP[SEM = <?dt(?n)>]    ->  DT[SEM=?dt]  N[SEM=?n]
      NP[SEM = <?n(?p)>]     ->  N[SEM=?n]    P[SEM = ?p]
      NP[SEM = <?np(?p)>]    ->  NP[SEM=?np]   P[SEM=?p]            
      NP[SEM = <?np(?w)>]   ->   NP[SEM=?dt]   WP[SEM=?w]
      NP[SEM = <?adj(?np)>]  ->  ADJ[SEM=?adj] NP[SEM=?np]
      NP[SEM = <?p(?np)>]    ->  P[SEM=?p]     NP[SEM=?np]
      
      VP[SEM = <?v(?vp)>]    ->  ITV[SEM=?v]    VP[SEM =?vp]
      VP[SEM = <?wp(?vp)>]   ->  WP[SEM =?wp]   VP[SEM=?vp]
      VP[SEM = <?v(?p)>]     ->  TV[SEM=?v]     P[SEM=?p]
      VP[SEM = <?v(?np)>]    ->  TV[SEM=?v]     NP[SEM=?np]
      VP[SEM = <?p(?np)>]    ->  P[SEM=?p]      NP[SEM=?np]

      P[SEM = <?p(?np)>]    ->  P[SEM=?p]       NP[SEM=?np]
      P[SEM = <?dt(?np)>]   ->  DT[SEM=?dt]     NP[SEM=?np]

      WP[SEM = <?w>]        ->  W[SEM =?w]
    // I'm sunure about his rule
    // WP[SEM = <?w(?s)>]    ->  W[SEM =?w]     S[SEM = ?s] 

    ############################ 
      DT -> A 
      Adj -> tall skinny big strong powerful short huge funny smart nice mean
      P -> about in as to ad into for near above as like since 
      C -> that 
      Aux -> be | have | do
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

