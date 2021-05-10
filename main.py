import nltk
import re
import os
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk import grammar, parse
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import wordnet
from nltk.parse import stanford
from functools import * 
# !wget 'https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip'
# !unzip 'stanford-tagger-4.2.0.zip'

# jar = '/content/stanford-postagger-4.2.0'
# model = '/content/stanford-postagger-full-2020-11-17/models/english-left3words-distsim.tagger'
def tokenize(words):
  words = words.lower()
  raw_tokens =  list(filter(lambda x: re.match(r"[A-Za-z]",x),nltk.word_tokenize(words)))
  
  tagged = nltk.pos_tag(raw_tokens) 
  type_map = {'J':wordnet.ADJ,'V':wordnet.VERB,'N':wordnet.NOUN,'R':wordnet.ADV,'D':wordnet.NOUN}
  lemma =  nltk.stem.WordNetLemmatizer()
  return [
      (lemma.lemmatize(token,type_map[type_value[0]])) if type_value[0] in type_map
      else (lemma.lemmatize(token))
      for token,type_value in tagged
    ]


def semantics_interface():
# take tokens and build a  Semantics interface
    grammer_str = r"""
     % start S
    # Grammar rules
      
      # Declarative (A Tall Skinny man coughed)
      S[SEM = <?s>] -> WP S[SEM=?s]
      S[SEM =  <?subj(?vp)>]  ->  NP[SEM=?subj] VP[SEM=?vp]

    S[SEM =  <?subj(vp)>]  ->  AUX NP[SEM=?subj]  TV[SEM=?vp]

      S[SEM = <?subj(?vp)>]/NP -> WP AUX NP[SEM=?subj] VP[SEM=?vp]/NP

      S[SEM =  <?subj(?v)>]  ->  NP[SEM=?subj]   
      S[SEM =  <?subj>]  ->  WP NP[SEM=?subj]
      S[SEM = <?vp>]       -> WP  VP[SEM=?vp] 
      S[SEM = <?vp>]   -> WP S[SEM=?s]
#      
#      S[SEM  = <?vp(?np)>]  ->  VP[SEM=?vp] NP[SEM=?np]
      NP[SEM = <?det(?n)>]   ->  DT[SEM=?det] N[SEM=?n]
      NP[SEM = <?pn>]        ->  PN[SEM=?pn]
      NP[SEM = <?np>]    ->  NP[SEM=?np]   PP[SEM=?p]            
      NP[SEM = <?np(?w)>]   ->   NP[SEM=?dt]    WP[SEM=?w]
      NP[SEM = <?adj(?np)>]  ->  Adj[SEM=?adj] NP[SEM=?np]
      NP[SEM = <?p(?np)>]    ->  P[SEM=?p]     NP[SEM=?np]

      VP[SEM = <?v(?vp)>]    ->  IV[SEM=?v]
      VP[SEM = <?v(?vp)>]    ->  IV[SEM=?v]    Adj[SEM =?vp]
      VP[SEM = <?v(?vp)>]    ->  IV[SEM=?v]    VP[SEM =?vp]
      VP[SEM = <?v(?p)>]     ->  TV[SEM=?v]     PP[SEM=?p]
      VP[SEM = <?v(?np)>]    ->  TV[SEM=?v]     NP[SEM=?np]
      VP[SEM = <?v>]/NP    ->  TV[SEM=?v]/NP
       

      PP[SEM = <?p(?np)>]    ->  P[SEM=?p]  NP[SEM=?np]    

      WP[SEM = <?w>]        ->  W[SEM =?w]
      WP[SEM = <?w(?s)>]    ->  W[SEM =?w]     S[SEM = ?s] 
    ############################ 
      DT[SEM=<\P Q.exists x.(P(x) & Q(x))>] -> 'a'
      DT[SEM=<\P Q.exists x.(P(x) & Q(x))>] -> 'the'
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
                 
      C -> 'that' 
      WP -> 'who' 
      WP -> 'what'

      AUX -> 'do' 

      IV[SEM=<\x.is(x)>] -> 'be'
      IV[SEM=<\x.is(x)>] -> 'is'
      IV[SEM=<\x.act(x)>] -> 'act' 
      IV[SEM=<\x.adapt(x)>] -> 'adapt' 
      IV[SEM=<\x.crawl(x)>] -> 'crawl' 
      IV[SEM=<\x.danse(x)>] -> 'danse' 
      IV[SEM=<\x.erupt(x)>] -> 'erupt' 
      IV[SEM=<\x.escape(x)>] ->'escape' 
      IV[SEM=<\x.leave(x)>] -> 'leave'
      IV[SEM=<\x.start(x)>] -> 'start' 
      IV[SEM=<\x.party(x)>] -> 'party'
      IV[SEM=<\x.panic(x)>] -> 'panic'

      TV[SEM=<\P x.P(\y.grab(x,y))>] -> 'grab'
      TV[SEM=<\P x.P(\y.impower(x,y))>] -> 'impower'
      TV[SEM=<\P x.P(\y.hold(x,y))>] -> 'hold'
      TV[SEM=<\P x.P(\y.push(x,y))>] -> 'push'
      TV[SEM=<\P x.P(\y.build(x,y))>] -> 'build'
      TV[SEM=<\P x.P(\y.mold(x,y))>] -> 'mold'
      TV[SEM=<\P x.P(\y.hug(x,y))>] -> 'hug'
      TV[SEM=<\P x.P(\y.love(x,y))>] -> 'love'
      TV[SEM=<\P x.P(\y.juice(x,y))>] ->'juice'
      TV[SEM=<\P x.P(\y.obliterate(x,y))>] -> 'obliterate'
      TV[SEM=<\P x.P(\y.like(x,y))>] ->'like'
      TV[SEM=<?v(\P.P(w))>]/NP -> TV[SEM=?v]

      N[SEM=<\x.man(x)>]-> 'man' 
      N[SEM=<\x.man(x)>] ->'boy' 
      N[SEM=<\x.pet(x)>] ->'cat' 
      N[SEM=<\x.pet(x)>] ->'dog' 
      N[SEM=<\x.time(x)>] ->'time'
      N[SEM=<\x.home(x)>] ->'house'
      N[SEM=<\x.company(x)>] ->'company'
      N[SEM=<\x.cow(x)>] ->    'cow'
      N[SEM=<\x.program(x)>] ->'program'
      N[SEM=<\x.study(x)>] ->'study'
      N[SEM=<\x.owner(x)>] ->'owner'
      N[SEM=<\x.man(x)>] -> 'door'
      N[SEM=<\x.check(x)>] ->'check'
      N[SEM=<\x.corner(x)>] ->'corner'
      N[SEM=<\x.job(x)>] -> 'job'
      N[SEM=<\x.dealership(x)>] ->'dealership'
      N[SEM=<\x.office(x)>] ->'office'
      N[SEM=<\x.customer(x)>] ->'customer'
      N[SEM=<\x.sailor(x)>] ->'sailor'
      N[SEM=<\x.man(x)>] ->'member' 
      N[SEM=<\x.man(x)>] ->'employee'
      PN[SEM=<\P.P(jimmy)>] -> 'jimmy'
      PN[SEM=<\P.P(jimmy)>] -> 'james' 
      PN[SEM=<\P.P(jimmy)>] -> 'jim'
      PN[SEM=<\P.P(jordan)>] ->'jordan'
      PN[SEM=<\P.P(jimmy)>] -> 'grant'
      PN[SEM=<\P.P(sarah)>] -> 'sarah' 
      PN[SEM=<\P.P(bob)>] -> 'bob'
      PN[SEM=<\P.P(dave)>] -> 'dave'  
      PN[SEM=<\P.P(jeff)>] -> 'jeff'
      PN[SEM=<\P.P(george)>] -> 'george' 
      VPB ->'sneeze'
      """    
    g= nltk.grammar.FeatureGrammar.fromstring(grammer_str) 
    return  (nltk.parse.FeatureChartParser(g,trace=1),g)    

def create_model():
    v = """
        jimmy => ji 
        jordan => jo 
        jeff => je
        dave => d 
        george => g 
        bob => b
        sarah => s

        man       =>{m1,m2}
        boy       =>{b1}
        cat       =>{ca1}
       pet       =>{p1}
        dog       =>{d1}
        time      =>{t1}
        house     =>{h1}
        company   =>{co1}
        cow       =>{cw1}
        program   =>{po1}
        study     =>{s1}
        owner     =>{o1}
        door      =>{do1}
        check     =>{ch1}
       corner    =>{c1}
        job       =>{j1}
        dealership=>{de1} 
        office    =>{o1,o2}
        customer  =>{cu1}
        sailor    =>{sa1}
        member    =>{me1}
        employee  =>{e1}
     
    
      # by => {(de1,o1)}
      # with => {(s,m)}
      # about => {(s1,p1)}
      # in    => {}
      # as    => {}
      # to    => {}
      # at    => {(cw1,h1)}
      # for   => {(po1,co1)}
      # near  => {(d1,m1)}
      # above => {(d1,m2)}
      # like  => {(ji,s)}
      # since => {}


       leave => {d,ji,e1}
       be       =>{}
       is       =>{}
       act      =>{}
       adapt    =>{}
       crawl    =>{}
       danse    =>{}
       erupt    =>{}
       escape   =>{m1}
       leave    =>{}
       start    =>{}
       party    =>{}
       panic    =>{}


        grab    =>     {(d,c1)}
        got =>         {(g,j1)}
        impower    =>  {(ji,jo)}
        hold    =>     {(d,c1)}
        push    =>     {(m1,b)}
        build    =>    {(je,h1)}
        mold    =>     {(ji,jco1)}
        hug    =>      {(s,m1)}
        love    =>     {(ji,s)}
        milk    =>     {(b1,cw1)}
        obliterate   =>{(e1,cu1)}
        

        funny => {ji}
        study   => {jo}
        tall    => {d}
        strong  => {g}
        powerful=> {m1} 
        short   => {s}
        huge    => {j1}
        smart   => {d1}
        nice    => {me1}
        mean    => {je}
        skinny  => {sa1}
        big     => {cu1}
        large   => {}


    """
    value = nltk.Valuation.fromstring(v)    
    init = nltk.Assignment(value.domain)
    m = nltk.Model(value.domain,value)
    return (m,init,value) 
    

def eval_sen(sen):

    tokens = tokenize(sen)
    print(tokens)
    (m,init,value) = create_model() 
    (parser,grammer) = semantics_interface() 
    parses = [tree.label()['SEM'] for tree in parser.parse(tokens)] 

    results = nltk.evaluate_sents([" ".join(tokens)], grammer, m, init)[0]


    formula = parses[0]
    
    print(formula)
    freevar = list(formula.free())
    print(freevar)

    for (syntree, semrep, value) in results:
        print(semrep,value) 
  
eval_sen("what did a man push")

