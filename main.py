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
      S[SEM  = <?sub(?vp)>]  -> NP[SEM=?subj] VP[SEM=?vp]
      PP[SEM = <?prep(?np)>] -> P[SEM=?prep] NP[SEM=?np]
      NP[SEM = <?det(?nom)>] -> DT[SEM=?det] N[SEM=?nom]
      N[SEM  = <?nom(?pp)>]  -> N[SEM=?nom] PP[SEM=?pp]
      N[SEM = <?adj(?nom)>]  -> Adj[SEM=?adj] N[SEM=?nom]
      VP[SEM = <?iv>] -> IV[SEM=?iv]
      VP[SEM = <?v(?obj)>] -> TV[SEM=?v] NP[SEM=?obj]
      VP[SEM = <?v(?obj(?obj))>] -> DTV[SEM=?v] NP[SEM=?obj] NP[SEM=?obj]
      VP[SEM = <?v(?obj(?prep))>] -> DTV[SEM=?obj] NP[SEM=?obj] PP[SEM=?prep]
      VP[SEM = <?vp(?pp)>] -> VP[SEM=?vp] PP[SEM=?vp]
      VP[SEM = <?v(?vp)>] -> SV[SEM=?v] S[SEM=?vp]
      VP[SEM = <?aux(?vp)>] -> AUX[SEM = <?aux>] VP[SEM = <?vp>]
      VP[SEM = <?v(?vp)>] -> ADV[SEM=?v] VP[SEM=?vp]  
      NP[SEM=<?pn>] -> PN[SEM=?pn]
      NP[SEM=<?prn>] -> PRN[SEM=?prn]
    ############################ 
      DT[SEM=<\P Q.exists x.((P(x) -> Q(x)))>] -> 'a'
      DT[SEM=<\P Q.exists x.((P(x) -> Q(x)))>] -> 'the'

      Adj[SEM=<\P x.((P)(x) & tall(x)) ] -> 'tall'   
      Adj[SEM=<\P x.((P)(x) & strong(x)) ] -> 'strong' 
      Adj[SEM=<\P x.((P)(x) & strong(x)) ] -> 'powerful' 
      Adj[SEM=<\P x.((P)(x) & short(x)) ] -> 'short' 
      Adj[SEM=<\P x.((P)(x) & huge(x)) ] -> 'huge' 
      Adj[SEM=<\P x.((P)(x) & funny(x)) ] -> 'funny' 
      Adj[SEM=<\P x.((P)(x) & smart(x)) ] -> 'smart'
      Adj[SEM=<\P x.((P)(x) & nice(x)) ] -> 'nice'
      Adj[SEM=<\P x.((P)(x) & mean(x)) ] -> 'mean'
      Adj[SEM=<\P x.((P)(x) & skinny(x)) ] -> 'skinny'
      Adj[SEM=<\P x.((P)(x) & big(x)) ] -> 'big'
      Adj[SEM=<\P x.((P)(x) & big(x)) ] -> 'large'

      P[PFORM=about,SEM<\P.P>] ->'about'   
      P[PFORM=in   ,SEM<\P.P>] ->'in'  
      P[PFORM=as   ,SEM<\P.P>] ->'as'  
      P[PFORM=to   ,SEM<\P.P>] ->'to'  
      P[PFORM=at   ,SEM<\P.P>] ->'at'  
      P[PFORM=for  ,SEM<\P.P>] ->'for'  
      P[PFORM=near ,SEM<\P.P>] ->'near'  
      P[PFORM=above,SEM<\P.P>] ->'above'  
      P[PFORM=as   ,SEM<\P.P>] ->'as'
      P[PFORM=like ,SEM<\P.P>] ->'like'
      P[PFORM=since,SEM<\P.P>] ->'since'
                 

      C -> that 

      WP -> who what 
      ITV[PFORM=] -> act adapt crawl danse erupt escape leave start party panic
      TV[sem=<\x x.x(\y.grab(x,y))] -> grab 
      TV[sem=<\x x.x(\y.impower(x,y))] -> impower 
      TV[sem=<\x x.x(\y.hold(x,y))] -> hold 
      TV[sem=<\x x.x(\y.push(x,y))] -> push 
      TV[sem=<\x x.x(\y.build(x,y))] -> build 
      TV[sem=<\x x.x(\y.mold(x,y))] -> mold 
      TV[sem=<\x x.x(\y.hug(x,y))] -> hug 
      TV[sem=<\x x.x(\y.love(x,y))] -> love 
      TV[sem=<\x x.x(\y.juice(x,y))] -> juice 
      TV[sem=<\x x.x(\y.obliterate(x,y))] -> obliterate 
      N[SEM=<\x.man(x)>]-> man 
      N[SEM=<\x.man(x)>] ->boy 
      N[SEM=<\x.pet(x)>] ->cat 
      N[SEM=<\x.pet(x)>] ->dog 
      N[SEM=<\x.time(x)>] ->time 
      N[SEM=<\x.home(x)>] ->house 
      N[SEM=<\x.company(x)>] ->company 
      N[SEM=<\x.cow(x)>] ->cow 
      N[SEM=<\x.program(x)>] ->program 
      N[SEM=<\x.study(x)>] ->study 
      N[SEM=<\x.owner(x)>] ->owner 
      N[SEM=<\x.man(x)>] ->door 
      N[SEM=<\x.check(x)>] ->check 
      N[SEM=<\x.corner(x)>] ->corner 
      N[SEM=<\x.job(x)>] ->job 
      N[SEM=<\x.dealership(x)>] ->dealership 
      N[SEM=<\x.office(x)>] ->office 
      N[SEM=<\x.customer(x)>] ->customer 
      N[SEM=<\x.sailor(x)>] ->sailor 
      N[SEM=<\x.man(x)>] ->member 
      N[SEM=<\x.man(x)>] ->employee

      np[sem=<\p.p(jimmy)>] -> Jimmy
      np[sem=<\p.p(jimmy)>] -> James 
      np[sem=<\p.p(jimmy)>] -> Jim
      np[sem=<\p.p(jordan)>] -> Jordan
      np[sem=<\p.p(jimmy)>] -> Grant
      np[sem=<\p.p(jimmy)>] -> Holtzman 
      np[sem=<\p.p(jimmy)>] -> Bob 
      np[sem=<\p.p(jimmy)>] -> Joe  
      np[sem=<\p.p(jimmy)>] -> Jeff 
      np[sem=<\p.p(jimmy)>] -> George 

      VPB ->sneeze
    """        
    
    
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
  """  
    # part 4
def CFG():
  
my_grammar = nltk.CFG.fromstring(string)

