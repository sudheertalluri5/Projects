# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:16:55 2019

@author: sudhe
"""

from bs4 import BeautifulSoup
import unicodedata
import re
import spacy
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity 

nlp=spacy.load("en_core_web_sm")

def rem_tags(doc):
    return nlp(BeautifulSoup(doc,'html.parser'.get_text()))
def expand_contracts(doc):
    return nlp(unicodedata.normalize('NFKD',doc).encode('ascii','ignore').decode('utf-8','ignore'))
def lemma(doc):
    return nlp(" ".join([word.lemma_ for word in doc]))
def rem_spchr(doc,rem_dig=False):
    pattern=r'[^a-zA-Z\s]' if rem_dig else r'[^a-zA-Z0-9]'
    text=re.sub(pattern,'',doc.text)
    return nlp(text)
def rem_stp(doc):
    return nlp(" ".join([word.lemma_ for word in doc]))

def pre_process(corpus,html_strip=True,contracted_expansion=True,Accent_removal=True,lower_case_text=True, lemmatization=True,rem_special_char=True,rem_stop=True,rem_digits=True):
        preprocessed_docs=[]
        for doc in corpus:
            if(html_strip):
                doc=rem_tags(doc)
            if(contracted_expansion):
                doc=expand_contracts(doc)
            if(lower_case_text):
                doc=doc.lower()
            doc=nlp(re.sub(r'[\r|\n|\r\n]','',doc.text))
            if(lemmatization):
                doc=lemma(doc)
            if(rem_special_char):
                doc=rem_spchr(doc,rem_digits)
            if(rem_stop):
                doc=rem_stp(doc)
        preprocessed_docs.append(doc)
    
wgh={"Company":1,"keyPerson":1,"product":1}
knowledgeBase={"Company":["Apple"],"Aliases":["Apple Inc"],"keyPerson":["Tim Cook","Steve Jobs"],"product":["Iphone","IMac","Ipod"]}
articles=["Apple, the richest company is going to release it's new OS Higher Sierra soon by Tim Cook.Tim Cook has become the CEO of Apple after Steve Jobs"
          ,"Apple released Iphone and IMac at a time in WWDC 2k19"]
sentences=[]
sentence_vectors=[]
for article in articles:
    art=nlp(article)
    entities=[]
    for entity in art.ents:
        entities.append(entity)
    mykeys=knowledgeBase.keys()
    count=dict()
    for key in mykeys:
        count[key]=0
    flag=False
    for entity in entities:
        for key in mykeys:
            if str(entity) in knowledgeBase[key] :
                flag=True
                count[key]+=1
                break
    if(flag):
        ent=[str(entity) for entity in entities]
        sentences.append(" ".join(ent))
nlp=spacy.load("en_core_web_lg")
for sentence in sentences:
    if len(sentence)!=0:
        v=sum([nlp.vocab[word].vector for word in sentence.split()])/(len(sentence.split()+0.01))
    else:
        v=np.zeroes((100,))
    sentence_vectors.append(v)
sim_mat=np.zeroes(len(sentences),len(sentences))
for i in range(len(sentences)):
    for j in range(len(sentences)):
        if i!=j:
            sim_mat[i][j]=cosine_similarity(sentence_vectors[i],sentence_vectors[j])[0,0]
nx_graph=nx.from_numpy_array(sim_mat)
scores=nx.pagerank(nx_graph)
ranked_sentences=sorted((scores[i],s) for i,s in enumerate(sentences),reverse=True)
print(ranked_sentences)