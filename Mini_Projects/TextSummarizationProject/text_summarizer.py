import numpy as np
import pandas as pd
import re
from nltk import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
#pandas to retrieve data
df=pd.read_csv("text_about_tennis.csv")
df.head()
                                                                    
#split text into sentences
sentences_list=[]
for article in df['article_text']:
    sentences_list.append(sent_tokenize(article))

sentences=[]
sentences = [y for x in sentences_list for y in x]

#removing punctuations

rem_pun=pd.Series(sentences).str.replace("[^a-zA-Z]"," ")
rem_pun_l=[s.lower() for s in rem_pun]

#removing stopwords
rem_stop=[]
stop_words=stopwords.words('english')
for sentence in rem_pun_l:
        tokens=re.split("\s",sentence)
        rem_stop.append(" ".join([token for token in tokens if token not in stop_words]))
#print(rem_stop)

#vector representation of glove 
word_embeddings={}
file=open("C:\py_prog\glove.6B.100d.txt",encoding='utf-8')
for line in file:
    vector_w=line.split()
    #See the glove.6B file where you can find first word is the entity and next is vector
    word=vector_w[0]
    vector=np.asarray(vector_w[1:],dtype='float32')
    word_embeddings[word]=vector
file.close()

#creating vectors for sentences by taking average
sentence_vectors=[]
for sentence in rem_stop:
    if len(sentence)!=0:
        sentence_vector=sum([word_embeddings.get(w,np.zeros(100,)) for w  in  sentence.split()])/(len(sentence.split())+0.001)
    else :
        sentence_vector=np.zeros(100,)
    sentence_vectors.append(sentence_vector)

#similarity matrix to prepare a graph so that we can find page rank
sim_matrix=np.zeros(len(sentences),len(sentences))
for i in range(len(sentences)):
    for j in range(len(sentences)):
        sim_matrix[i][j]=cosine_similarity(sentence_vectors[i].reshape(1,100),sentence_vectors[j].reshape(1,100))
print(sim_matrix)

  
