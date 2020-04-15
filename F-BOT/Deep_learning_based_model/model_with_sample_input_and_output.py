# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 02:31:17 2020

@author: sudhe
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 22:53:27 2020

@author: sudhe
"""

import json
import nltk
import pickle
import random
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.models import model_from_json
from nltk.stem.lancaster import LancasterStemmer


random.seed(10)
stemmer=LancasterStemmer()
ignore_words=['?']


class fbot:
    def __init__(self,update=False,err_thres=0.5):
        self.classes=list()
        self.word_list=list()
        self.training_data=list()
        self.update_data=update
        self.ERROR_THRESHOLD=err_thres
    def get_intents(self):
        with open('./intents.json') as json_file:
            self.intents=json.load(json_file)
        print('loaded intents')
        return self.intents
    def bag_of_words(self,sentence):
        bag=np.zeros((1,len(self.word_list)))
        sentence=nltk.word_tokenize(sentence)
        try:
            for word in sentence:
                bag[0,self.word_list.index(stemmer.stem(word))]=1
        finally:
            return bag
    def get_input_and_output_vectors(self):
        random.shuffle(self.training_data)
        self.training_data=np.array(self.training_data)
        self.X_train= self.training_data[:,0]
        self.y_train = self.training_data[:,1]
        self.X_train=np.array(self.X_train.tolist())
        self.y_train=np.array(self.y_train.tolist())
        print('x_train,y_train done')
    def preprocessing_for_training_database(self):
        self.classes=sorted([intent['tag'] for intent in self.intents['intents']])
        patterns=list()
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                pattern2=nltk.word_tokenize(pattern.lower())
                patterns.append([pattern,intent['tag']])
                self.word_list.extend([stemmer.stem(word) for word in pattern2 if word not in ignore_words])
                self.word_list=sorted(list(set(self.word_list)))
        for pattern,tag in patterns:
            labels=[0]*len(self.classes)
            labels[self.classes.index(tag)]=1
            self.training_data.append([self.bag_of_words(pattern).ravel().tolist(),labels])
        print('training data')
        self.get_input_and_output_vectors()
    def model_training(self):
        self.model = Sequential()
        self.model.add(Dense(self.X_train.shape[1], activation='relu', input_dim=self.X_train.shape[1]))
        self.model.add(Dense(10, activation='relu'))
        self.model.add(Dense(len(self.classes),activation='softmax'))
        self.model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
        self.model.fit(self.X_train,self.y_train, epochs=1000, batch_size=32)
    def load_data(self):
        self.get_intents()
        self.preprocessing_for_training_database()
        with open('data.pickle','wb') as f:
            pickle.dump((self.intents,self.classes,self.word_list,self.X_train,self.y_train),f)
    def load_model(self):
        self.model_training()
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        self.model.save_weights("model.h5")
        print("model saved")
    def start(self):
        if(self.update_data):
            self.load_data()
            self.load_model()
        else:
            try:
                with open('data.pickle','rb') as f:
                    self.intents,self.classes,self.word_list,self.X_train,self.y_train=pickle.load(f)
            except:
                self.load_data()
            try:
                with open('model.json') as f:
                    self.model=model_from_json(f.read())
                    self.model.load_weights("model.h5")
            except:
                self.load_model()
        print("Hi! I'm F-BOT! You can talk to me now\n")
        while(True):
            converse=input().lower()
            if(converse=='quit'):
                break
            bow=self.bag_of_words(converse)
            output=self.model.predict(bow)
            output=output.ravel().tolist()
            index=np.argmax(output)
            if(output[index]>self.ERROR_THRESHOLD):
                output_tag=self.classes[index]
                for intent in self.intents['intents']:
                    if(intent['tag']==output_tag):
                        print(random.choice(intent['responses']))
            else:
                print("Sorry I didn't understand")
bot=fbot()
bot.start()




