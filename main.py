import os
import re

import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from functools import *

from nltk import grammar, parse
from nltk.corpus import wordnet
from nltk.tokenize import wordpunct_tokenize

def tokenize(words):
  words = words.lower()
  raw_tokens =  list(filter(lambda x: re.match(r"[A-Za-z]",x),nltk.word_tokenize(words)))
  
  tagged = nltk.pos_tag(raw_tokens) 
  type_map = {'J':wordnet.ADJ,'V':wordnet.VERB,'N':wordnet.NOUN,'R':wordnet.ADV,'D':wordnet.NOUN}
  lemma =  nltk.stem.WordNetLemmatizer()
  return [
      (lemma.lemmatize(token,type_map[type_value[0]])) if type_value[0] in type_map
      else (lemma.lemmatize(token),type_value)
      for token,type_value in tagged
    ]

def determine_type(sen):
  words = nltk.tokenize.word_tokenize(sen)
  wordTagList = nltk.pos_tag(words)
  tagList = [tag for (word,tag) in wordTagList]
  if tagList[0] is "WP":
        return "Who"
  elif tagList[0] is "AUX":
        return "YesNo"
  else:
          return "Declaration"


def semantics_interface():
# take tokens and build a  Semantics interface
    grammer_str = r"""
     % start S
      # Grammar rules
      
      # Declarative (A Tall Skinny man coughed)
      S[SEM =  <?subj(?vp)>]  ->  NP[SEM=?subj] VP[SEM=?vp]
      
      S[SEM  = <?w(?vp)>]  ->  WP[SEM=?w] VP[SEM=?vp]
      
      S[SEM  = <?vp(?np)>]  ->  VP[SEM=?vp] NP[SEM=?np]

      S[SEM =  <?subj(?vp)>] -> AUX NP[SEM=?subj] VP[SEM=?vp]

      NP[SEM = <?det(?n)>]   ->  DT[SEM=?det] N[SEM=?n]
      NP[SEM = <?n(?p)>]     ->  N[SEM=?n]     P[SEM = ?p]
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
      VP[SEM = <?v>]    ->  IV[SEM=?v]    

      P[SEM = <?p(?np)>]    ->  P[SEM=?p]       NP[SEM=?np]
      P[SEM = <?dt(?np)>]   ->  DT[SEM=?dt]     NP[SEM=?np]

      WP[SEM = <?w>]        ->  W[SEM =?w]
      WP[SEM = <?w(?s)>]    ->  W[SEM =?w]     S[SEM = ?s] 

    ############################ 

    # Lexicon rules

      DT[SEM=<\P Q.exists x.((P(x) -> Q(x)))>] -> 'a'
      DT[SEM=<\P Q.exists x.((P(x) -> Q(x)))>] -> 'the'

      Adj[SEM=<\P x.((P)(x) & tall(x))>] -> 'tall'   
      Adj[SEM=<\P x.((P)(x) & strong(x))>] -> 'strong' 
      Adj[SEM=<\P x.((P)(x) & strong(x))>] -> 'powerful' 
      Adj[SEM=<\P x.((P)(x) & short(x))>] -> 'short' 
      Adj[SEM=<\P x.((P)(x) & huge(x))>] -> 'huge' 
      Adj[SEM=<\P x.((P)(x) & funny(x))>] -> 'funny' 
      Adj[SEM=<\P x.((P)(x) & smart(x))>] -> 'smart'
      Adj[SEM=<\P x.((P)(x) & nice(x))>] -> 'nice'
      Adj[SEM=<\P x.((P)(x) & mean(x))>] -> 'mean'
      Adj[SEM=<\P x.((P)(x) & skinny(x))>] -> 'skinny'
      Adj[SEM=<\P x.((P)(x) & big(x))>] -> 'big'
      Adj[SEM=<\P x.((P)(x) & big(x))>] -> 'large'

      P[PFORM=about,SEM=<\P.P>] ->'about'   
      P[PFORM=in   ,SEM=<\P.P>] ->'in'  
      P[PFORM=as   ,SEM=<\P.P>] ->'as'  
      P[PFORM=to   ,SEM=<\P.P>] ->'to'  
      P[PFORM=at   ,SEM=<\P.P>] ->'at'  
      P[PFORM=for  ,SEM=<\P.P>] ->'for'  
      P[PFORM=near ,SEM=<\P.P>] ->'near'  
      P[PFORM=above,SEM=<\P.P>] ->'above'  
      P[PFORM=as   ,SEM=<\P.P>] ->'as'
      P[PFORM=like ,SEM=<\P.P>] ->'like'
      P[PFORM=since,SEM=<\P.P>] ->'since'
                 
      AUX -> 'did' | 'was'
      
      C -> 'that' 
      WP -> 'who' | 'what' 
      IV[SEM=<\x.is] -> 'is' 
      IV[SEM=<\x.act] -> 'act' 
      IV[SEM=<\x.adapt] -> 'adapt' 
      IV[SEM=<\x.crawl] -> 'crawl' 
      IV[SEM=<\x.dance] -> 'dance' 
      IV[SEM=<\x.erupt] -> 'erupt' 
      IV[SEM=<\x.escape] -> 'escape' 
      IV[SEM=<\x.leave] -> 'leave' 
      IV[SEM=<\x.start] -> 'start' 
      IV[SEM=<\x.party] -> 'party' 
      IV[SEM=<\x.panic] -> 'panic'
      TV[SEM=<\x x.x(\y.grab(x,y))] -> 'grab' 
      TV[SEM=<\x x.x(\y.impower(x,y))] -> 'impower' 
      TV[SEM=<\x x.x(\y.hold(x,y))] -> 'hold' 
      TV[SEM=<\x x.x(\y.push(x,y))] -> 'push' 
      TV[SEM=<\x x.x(\y.build(x,y))] -> 'build' 
      TV[SEM=<\x x.x(\y.mold(x,y))] -> 'mold' 
      TV[SEM=<\x x.x(\y.hug(x,y))] -> 'hug' 
      TV[SEM=<\x x.x(\y.love(x,y))] -> 'love' 
      TV[SEM=<\x x.x(\y.juice(x,y))] -> 'juice' 
      TV[SEM=<\x x.x(\y.obliterate(x,y))] -> 'obliterate' 

      N[SEM=<\x.man(x)>]-> 'man' 
      N[SEM=<\x.man(x)>] -> 'boy' 
      N[SEM=<\x.pet(x)>] -> 'cat' 
      N[SEM=<\x.pet(x)>] -> 'dog' 
      N[SEM=<\x.time(x)>] -> 'time' 
      N[SEM=<\x.home(x)>] -> 'house' 
      N[SEM=<\x.company(x)>] -> 'company' 
      N[SEM=<\x.cow(x)>] -> 'cow' 
      N[SEM=<\x.program(x)>] -> 'program' 
      N[SEM=<\x.study(x)>] -> 'study' 
      N[SEM=<\x.owner(x)>] -> 'owner' 
      N[SEM=<\x.man(x)>] -> 'door' 
      N[SEM=<\x.check(x)>] -> 'check' 
      N[SEM=<\x.corner(x)>] -> 'corner' 
      N[SEM=<\x.job(x)>] -> 'job' 
      N[SEM=<\x.dealership(x)>] -> 'dealership' 
      N[SEM=<\x.office(x)>] -> 'office' 
      N[SEM=<\x.customer(x)>] -> 'customer' 
      N[SEM=<\x.sailor(x)>] -> 'sailor' 
      N[SEM=<\x.man(x)>] -> 'member' 
      N[SEM=<\x.man(x)>] ->'employee'

      NP[SEM=<\P.P(jimmy)>] -> 'jimmy'
      NP[SEM=<\P.P(jimmy)>] -> 'james' 
      NP[SEM=<\P.P(jimmy)>] -> 'jim'
      NP[SEM=<\P.P(jordan)>] ->'jordan'
      NP[SEM=<\P.P(jimmy)>] -> 'grant'
      NP[SEM=<\P.P(sarah)>] -> 'sarah' 
      NP[SEM=<\P.P(bob)>] -> 'bob'
      NP[SEM=<\P.P(dave)>] -> 'dave'  
      NP[SEM=<\P.P(jeff)>] -> 'jeff'
      NP[SEM=<\P.P(george)>] -> 'george' 
      VPB ->'sneeze'
      """
    g= nltk.grammar.FeatureGrammar.fromstring(grammer_str) 
    return  (nltk.parse.FeatureChartParser(g,trace=0),g)    

def create_model():
    v = """
        jimmy => ji 
        jordan => jo 
        jeff => je
        dave => d 
        george => g 
        bob => b
        sarah => s

     #   man       =>{m1}
     #   boy       =>{b1}
     #   cat       =>{ca1}
         pet       =>{p1}
     #   dog       =>{d1}
     #   time      =>{t1}
     #   house     =>{h1}
     #   company   =>{co1}
     #   cow       =>{cw1}
     #   program   =>{p1}
     #   study     =>{s1}
     #   owner     =>{o1}
     #   door      =>{do1}
     #   check     =>{ch1}
         corner    =>{c1}
     #   job       =>{j1}
     #   dealership=>{de1} 
     #   office    =>{o1}
     #   customer  =>{cu1}
     #   sailor    =>{sa1}
     #   member    =>{me1}
     #   employee  =>{e1}


        grab    =>     {(d,c1)}
     #   got =>         {(g,j1)}
     #   impower    =>  {(ji,jo)}
     #   hold    =>     {(d,c1)}
     #   push    =>     {(m1,b)}
     #   build    =>    {(je,h1)}
     #   mold    =>     {(ji,jco1)}
     #   hug    =>      {(s,m1)}
     #   love    =>     {(ji,s)}
     #   milk    =>     {(b1,cw1)}
     #   obliterate   =>{(e1,cu1)}

     #   funny => {ji}
     #   study   => {jo}
     #   tall    => {d}
     #   strong  => {g}
     #   powerful=> {m1} 
     #   short   => {s}
     #   huge    => {j1}
     #   smart   => {d1}
     #   nice    => {me1}
     #   mean    => {je}
     #   skinny  => {sa1}
     #   big     => {cu1}
     #   large   => {}


    """
    value = nltk.Valuation.fromstring(v)    
    init = nltk.Assignment(value.domain)
    m = nltk.Model(value.domain,value)
    return (m,init) 
    

def eval_sen(sen):

    tokens = tokenize(sen)
    print(tokens)
    (m,init) = create_model() 
    (parser,grammer) = semantics_interface() 
    parses = [tree.label()['SEM'] for tree in parser.parse(tokens)] 

    results = nltk.evaluate_sents([" ".join(tokens)], grammer, m, init)[0]
    for (syntree, semrep, value) in results:
        if determine_type(sen) is "Declaration":
          if value is True:
            print("I know!")
          else:
            print("I don't think so")
        elif determine_type(sen) is "YesNo":
            if value is True:
              print("Yes!")
            else:
              print("No!")
        else:
          if value is True:
            print("The answer is")
          else:
            print("What are you talking about ?")  
  
eval_sen("dave grabbed the dog")

