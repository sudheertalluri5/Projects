# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 22:24:18 2019

@author: sudhe
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 19:55:37 2019

@author: sudhe
"""
import spacy
import neuralcoref
coref_nlp=spacy.load('en')
neuralcoref.add_to_pipe(coref_nlp)
nlp=spacy.load('en_core_web_sm')

def My_Pos_Rank(sent_art,coref_art,req):
    rank=0
    den=0
    n=len(sent_art)
    sentence=dict()
    for i in range(n):
        sentence[i]=True
        if req in sent_art[i]:
            rank+=(n-i)
            den+=n
            sentence[i]=False
    for key in list(coref_art.keys()):
        if req in key:
            for i in coref_art[key]:
                if(sentence[i]):
                    rank+=(n-i)
                    den+=n
            break
    if(rank==0):
        return 0
    return rank/den

articles=[]
x="myInput.txt"
y=open(x).read()
articles.append(y)

knowledgeBase={'Company':['Apple'],'keyPeople':['Tim Cook','Steve Jobs'],'products':['iMac','iPhone','iPod','iPad']}

lexrank=[]
posrank=[]
def weights(entity):
    return 1
myvalues=[]
for value in list(knowledgeBase.values()):
    for val in value:
        myvalues.append(val.lower())
for article in articles:
    doc=nlp(article)
    sentences=[]
    start_sen=dict()
    docc=coref_nlp(article)
    coref_art=dict()
    if(docc._.has_coref):
        temp=docc._.coref_clusters
        print(temp)
        for i in range(len(temp)):
            coref_art[temp[i][0].text.lower()]=[]
            for j in range(len(temp[i])-1):
                coref_art[temp[i][0].text.lower()].append(temp[i][j+1].start)
    for i,sent in enumerate(doc.sents):
        sentences.append(sent.text.lower())
        for j in range(sent.start,sent.end):
            start_sen[j]=i
    temp2=dict()
    for key in list(coref_art.keys()):
        temp2[key]=set()
        for coref in coref_art[key]:
            temp2[key].add(start_sen[coref])
    print(start_sen)
    print(temp2)
    coref_art=temp2
    #lexArticle=Int_Page_Rank(article)
#    print(lexArticle)
    for i in range(len(sentences)):
        print(i,sentences[i])
    for value in myvalues:
        #lexrank.append(My_Rank(lexArticle,value,True))
        posrank.append(My_Pos_Rank(sentences,coref_art,value))
#print(lexrank)
print(posrank)