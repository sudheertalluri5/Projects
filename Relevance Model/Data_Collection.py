# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:44:24 2019

@author: sudhe
"""
from SPARQLWrapper import SPARQLWrapper,JSON
import re
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
companies=["Apple_Inc.","Equifax"]
for company in companies:
    queryString="""SELECT ?property ?hasValue WHERE { <http://dbpedia.org/resource/"""+company+"""> 
                    ?property ?hasValue}"""
    sparql.setQuery(queryString)
    sparql.setReturnFormat(JSON)
    res = sparql.query().convert()
    results=dict()
    X=[]
    Y=[]
    for result in res["results"]["bindings"]:
        x=(re.split("/",result["property"]["value"]))
        X.append(x[len(x)-1])
        y=(re.split("/",result["hasValue"]["value"]))
        Y.append(y[len(y)-1])
    for x in X:
        results[x]=[]
    for i,x in enumerate(X):
        results[x].append(Y[i])
    print(results['industry'])