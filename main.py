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


def semantics_interface():
# take tokens and build a  Semantics interface
    grammer_str = """
    # % start S
    # Grammar rules
      
      // Declarative (A Tall Skinny man coughed)
      S[SEM =  <?np(?vp)>]  ->  NP[SEM=?np] VP[SEM=?vp]
      
      // Wh-Questions
      S[SEM  = <?w(?vp)>]  ->  WP[SEM=?w] VP[SEM=?vp]
      
      // Yes-No Questions
      S[SEM  = <?vp(?np)>]  ->  VP[SEM=?vp] NP[SEM=?np]

      NP[SEM = <?n>]         ->  N[SEM=?n]
      NP[SEM = <?n(?p)]      ->  N[SEM=?n]     P[SEM = ?p]
      NP[SEM = <?pn>]        ->  PN[SEM=?pn]
      NP[SEM = <?np(?p)>]    ->  NP[SEM=?np]   P[SEM=?p]            
      NP[SEM = <?np(?w)>]   ->   NP[SEM=?dt]    WP[SEM=?w]
      NP[SEM = <?adj(?np)>]  ->  ADJ[SEM=?adj] NP[SEM=?np]
      NP[SEM = <?p(?np)>]    ->  P[SEM=?p]     NP[SEM=?np]
      
      VP[SEM = <?v(?vp)>]    ->  ITV[SEM=?v]    VP[SEM =?vp]
      VP[SEM = <?v(?p)>]     ->  TV[SEM=?v]     P[SEM=?p]
      VP[SEM = <?v(?np)>]    ->  TV[SEM=?v]     NP[SEM=?np]
      VP[SEM = <?p(?np)>]    ->  P[SEM=?p]      NP[SEM=?np]

      P[SEM = <?p(?np)>]    ->  P[SEM=?p]       NP[SEM=?np]
      P[SEM = <?dt(?np)>]   ->  DT[SEM=?dt]     NP[SEM=?np]

      WP[SEM = <?w>]        ->  W[SEM =?w]
      WP[SEM = <?w(?s)>]    ->  W[SEM =?w]     S[SEM = ?s] 

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
      ITV -> act adapt crawl danse erupt escape leave start party panic
      TV[SEM=<\\x x.x(\y.grab(x,y))] -> grab 
      TV[SEM=<\\x x.x(\y.impower(x,y))] -> impower 
      TV[SEM=<\\x x.x(\y.hold(x,y))] -> hold 
      TV[SEM=<\\x x.x(\y.push(x,y))] -> push 
      TV[SEM=<\\x x.x(\y.build(x,y))] -> build 
      TV[SEM=<\\x x.x(\y.mold(x,y))] -> mold 
      TV[SEM=<\\x x.x(\y.hug(x,y))] -> hug 
      TV[SEM=<\\x x.x(\y.love(x,y))] -> love 
      TV[SEM=<\\x x.x(\y.juice(x,y))] -> juice 
      TV[SEM=<\\x x.x(\y.obliterate(x,y))] -> obliterate 

      N[SEM=<\\x.man(x)>]-> man 
      N[SEM=<\\x.man(x)>] ->boy 
      N[SEM=<\\x.pet(x)>] ->cat 
      N[SEM=<\\x.pet(x)>] ->dog 
      N[SEM=<\\x.time(x)>] ->time 
      N[SEM=<\\x.home(x)>] ->house 
      N[SEM=<\\x.company(x)>] ->company 
      N[SEM=<\\x.cow(x)>] ->cow 
      N[SEM=<\\x.program(x)>] ->program 
      N[SEM=<\\x.study(x)>] ->study 
      N[SEM=<\\x.owner(x)>] ->owner 
      N[SEM=<\\x.man(x)>] ->door 
      N[SEM=<\\x.check(x)>] ->check 
      N[SEM=<\\x.corner(x)>] ->corner 
      N[SEM=<\\x.job(x)>] ->job 
      N[SEM=<\\x.dealership(x)>] ->dealership 
      N[SEM=<\\x.office(x)>] ->office 
      N[SEM=<\\x.customer(x)>] ->customer 
      N[SEM=<\\x.sailor(x)>] ->sailor 
      N[SEM=<\\x.man(x)>] ->member 
      N[SEM=<\\x.man(x)>] ->employee

      np[SEM=<\P.P(jimmy)>] -> 'jimmy'
      np[SEM=<\P.P(jimmy)>] -> 'james' 
      np[SEM=<\P.P(jimmy)>] -> 'jim'
      np[SEM=<\P.P(jordan)>] ->'jordan'
      np[SEM=<\P.P(jimmy)>] -> 'grant'
      np[SEM=<\P.P(sarah)>] -> 'sarah' 
      np[SEM=<\P.P(bob)>] -> 'bob'
      np[SEM=<\P.P(dave)>] -> 'dave'  
      np[SEM=<\P.P(jeff)>] -> 'jeff'
      np[SEM=<\P.P(george)>] -> 'george' 

      VPB ->sneeze
      """
    return  nltk.parse.FeatureChartParser(grammer_str)     

    def create_model():
        v = """
        jimmy => ji 
        jordan => jo 
        jeff => je
        dave => d 
        george => g 
        bob => b
        sarah => s



        grab       =>{}  
        impower    =>{} 
        hold       =>{}
        push       =>{}
        build      =>{}
        mold       =>{}
        hug        =>{}
        love       =>{}
        juice      =>{}
        obliterate =>{}

        man       =>{m1}
        boy       =>{b1}
        cat       =>{ca1}
        dog       =>{d1}
        time      =>{t1}
        house     =>{h1}
        company   =>{co1}
        cow       =>{cw1}
        program   =>{p1}
        study     =>{s1}
        owner     =>{o1}
        door      =>{do1}
        check     =>{ch1}
        corner    =>{c1}
        job       =>{j1}
        dealership=>{de1} 
        office    =>{o1}
        customer  =>{cu1}
        sailor    =>{sa1}
        member    =>{me1}
        employee  =>{e1}

        

        grab    =>     {}
        impower    =>  {}
        hold    =>     {}
        push    =>     {}
        build    =>    {}
        mold    =>     {}
        hug    =>      {}
        love    =>     {}
        juice    =>    {}
        obliterate   =>{}

        funny => {ji}
        study   => {jo}
        tall    => {d}
        strong  => {}
        powerful=> {} 
        short   => {}
        huge    => {}
        funny   => {}
        smart   => {}
        nice    => {}
        mean    => {}
        skinny  => {}
        big     => {}
        large  '=> {}


        """
        value = nltk.Valuation.fromstring(v)    
        init = nltk.Assignment(value.domain)
        m = nltk.Model(value.domain,value)
        return (m,init) 
    
    def eval_sen(sen):
        m = create_model() 
        si= semantics_interface() 
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
  

