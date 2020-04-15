# Importing Packages
import os
import random
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity 

#loading pretrained spacy english model
nlp=spacy.load('en_core_web_sm')

stop_words=['is','was','were','are','be','me','do','from']

#ymltodict

# copus is in .yml format which is required to convert to dictionary
class yml2dict:
    def yml2dict(self,path):
        self.database=dict()
        prepath=path
        files=os.listdir(prepath)
        for file in files:
            with open(prepath+file,'r',encoding='latin1') as f:
                lines=f.readlines()
                for line in lines[4:]:
                    line=line.lower()
                    if(line.startswith("- -")):
                        line=line.replace("- - ","")
                        line=line.replace("\n","")
                        temp=line
                        self.database[line]=list()
                    else:
                        line=line.replace("- ","")
                        line=line.replace("\n","")
                        self.database[temp].append(line)
        return self.database

#glove_embeddings
class glove_embeddings:
    def __init__(self):
        self.word_embeddings=dict()
    def glove_embeddings(self,path):
        with open(path, encoding='utf-8') as f:
            lines=f.readlines()
            for line in lines:
                values = line.split()
                word = values[0].lower()
                coefs = np.asarray(values[1:], dtype='float32')
                self.word_embeddings[word] = coefs
        return self.word_embeddings

#Chatbot both rule and retrieval based
class Chatbot:
    def __init__(self,database,embeddings,confidence_level=0.3):
        self.database=database
        self.word_embeddings=embeddings
        self.confidence_level=confidence_level
    def avg_embeddings_of_kb(self):
        self.average_embeddings=dict()    
        for key in self.database.keys():
                self.average_embeddings[key]= sum([self.word_embeddings.get(str(w.lemma_), np.zeros((100,))) for w in nlp(key) if str(w) not in stop_words])/(len(key.split())+0.001)
                if(type(self.average_embeddings[key])==float):
                    self.average_embeddings[key]=np.zeros((100,))
    def preprocess(self,command):
        loaded_command=nlp(command.lower())
        preprocessed_text=[str(word) for word in loaded_command if str(word) not in stop_words]
        return ' '.join(preprocessed_text)
    def reply(self,message):
        message=np.asarray(message)
        maximum=0
        best_query=list()
        for query in self.average_embeddings:
            match=abs(cosine_similarity(message.reshape(1,100), self.average_embeddings[query].reshape(1,100))[0,0])
            if match>maximum:
                maximum=match
                best_query=list()
                best_query.append(query)
            elif match==maximum:
                best_query.append(query)
        if(len(best_query)>0):
            best_query=random.choice(best_query)
        return (random.choice(self.database[best_query]),maximum)
    def start(self):
        print("""Hi, I'm F-Bot! How can I help you? 
                  To quit enter exit in the console\n""")
        self.avg_embeddings_of_kb()
        while(True):
            command=input()
            if(command.lower()=="quit"):
                break
            if(command.lower() in [key.lower() for key in list(self.database.keys())]):
                print(random.choice(self.database[command.lower()]))
            else:
                preprocessed_text=self.preprocess(command)
                print(type(preprocessed_text))
                if(len(preprocessed_text)==0):
                    average_embeddings=np.zeros((100,))
                else:
                    average_embeddings= sum([self.word_embeddings.get(str(w), np.zeros((100,))) for w in nlp(preprocessed_text) if str(w) not in stop_words])/(len(preprocessed_text)+0.001)
                print(average_embeddings)
                reply,similarity=self.reply(average_embeddings)
                if(similarity>=self.confidence_level):
                    print(reply)
                else:
                    print(random.choice(["Sorry, I didn't get you!","Pardon! Can you reframe it"]))
        print("Thanks For Using F-BOT!!")


database_path="C:\Datasets\chatterbot-corpus-master\chatterbot_corpus\data\english\\"
database=yml2dict().yml2dict(database_path)
embeddings_path='glove.6B.100d.txt'
embeddings=glove_embeddings().glove_embeddings(embeddings_path)
print("Enter Confidence Level")
confidence_level=float(input())
fbot=Chatbot(database,embeddings,confidence_level)
fbot.start()

