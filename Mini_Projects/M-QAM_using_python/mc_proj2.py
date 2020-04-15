# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:33:28 2019

@author: sudhe
"""

import numpy as np
import math
from matplotlib.image import imread
import matplotlib.pyplot as plt
from scipy.stats import rayleigh

class MQAM_modulate:
    def __init__(self,m):
        self.mqam_list=list()
        self.m=m
        #self.modulate()
    def row_col_finder(self):
        num=self.m
        row=math.sqrt(num)
        while(int(row+0.5)**2!=num):
            num=num/2
            row=math.sqrt(num)        
        self.row=int(row)
        self.column=self.m//self.row
    def mqam_carrier(self):
        for i in range(-1*self.row//2,self.row//2):
            rowv=2*i+1
            for j in range(-1*self.column//2,self.column//2):
                colv=2*j+1
                self.mqam_list.append(complex(rowv,colv))
    def mqam(self,img):
        img=255*imread("try.png")
        img=img.astype(np.uint8)
        img=img[:,:,0]
        img=img.flatten()
        binary=list(map(bin,img))
        bin_strings=list(map(lambda x:x[2:].zfill(8),binary))
        img2=list(map(lambda y:list(map(lambda x:int(x),y)),bin_strings))
        image=list()
        for i in img2:
            image.extend(i)
        image=np.asarray(image)
        temp=int(math.log2(self.m))
        pad=np.zeros((temp-(image.shape[0])%temp)%temp,dtype='uint8')
        image=np.concatenate((image,pad))
        self.forber=image
        image=image.reshape(len(image)//int(math.log2(self.m)),int(math.log2(self.m)))
        self.mqam_op=list(map(lambda y: int(y,2),list(map(lambda x:''.join(list(map(str,x))),list(image)))))
        self.modulated=list(map(lambda x:self.mqam_list[x],self.mqam_op))
    def modulate(self):
        img=imread("try.png")
        image=img.flatten()
#        print("enter M:")
#        self.m=int(input())
#        
        self.row_col_finder()
        self.mqam_carrier()
        self.mqam(image)
        #print(self.mqam_list)
#        print(image[...,:1])
#        print(self.mqam_op)
#        print(self.modulated)
        return (self.modulated,self.m)
        
class Rayleigh_channel:
    def __init__(self,modulated):
        self.modulated=modulated
    def rayleigh_ch(self):
        rch=rayleigh.rvs(size=len(self.modulated))
        self.rch_mod=self.modulated+rch
        return self.rch_mod
class MQAM_demodulate:
    def __init__(self,modulated,m):
        self.m=m
        self.modulated=modulated
        self.dmqam_dict=dict()
        self.dqam_list=list()
        self.demodulated=list()
        self.modulatedth=list()
    def row_col_finder(self):
        num=self.m
        row=math.sqrt(num)
        while(int(row+0.5)**2!=num):
            num=num/2
            row=math.sqrt(num)        
        self.row=int(row)
        self.column=self.m//self.row
        #print(self.row,self.column)
    def mqam_carrier(self):
        for i in range(-1*self.row//2,self.row//2):
            rowv=2*i+1
            for j in range(-1*self.column//2,self.column//2):
                colv=2*j+1
                self.dmqam_dict[complex(rowv,colv)]=(i+(self.row//2))*self.column+(j+(self.column//2))
        #print(self.dmqam_dict)
    def thres(self,x):
        if(x>0):
            if(x>self.row-1):
                x=self.row-1
            elif(int(x)%2==0):
                x=int(x)+1
            else:
                x=int(x)
        else:
            if(x<-self.row+1):
                x=-self.row+1
            elif(int(x)%2==0):
                x=int(x)-1
            else:
                x=int(x)
        return x
    def threshold(self):
        for x in self.modulated:
            real,imag=x.real,x.imag
            th=np.vectorize(self.thres)
            realth,imagth=th([real,imag])
            self.modulatedth.append(complex(realth,imagth))
    def dmqam(self):
        print(self.m)
        for key in self.modulatedth:
            self.dqam_list.append(self.dmqam_dict[key])
            #print(self.dqam_list)
        bin_mod=list(map(lambda a: a[2:].zfill(int(math.log2(self.m))),list(map(bin,self.dqam_list))))
        split_mod=list(map(lambda y:list(map(lambda x:int(x),y)),bin_mod))
        #print(split_mod)
        self.uni_mod=list()
        for x in split_mod:
            self.uni_mod.extend(x)
        #print(uni_mod)
        string_mod=''.join(list(map(str,self.uni_mod)))
        conv1=list()
        for i in range(0,len(string_mod),8):
            conv1.append(int(string_mod[i:i+8],2))
        conv_array=(np.asarray(conv1[:65536]).reshape(256,256))/255
        #print(conv_array)
        for x in conv_array:
            temp=list()
            for y in x:
                temp.append([y]*3)
            self.demodulated.append(temp)
        print("Image Generated")
        #print(np.asarray(self.demodulated))
        plt.imsave(fname="out.png",arr=np.asarray(self.demodulated))
        print("saved")
    def demodulate(self):
        self.row_col_finder()
        self.mqam_carrier()
        self.threshold()
        self.dmqam()
        return
mod=MQAM_modulate()
modulated,m=mod.modulate()
rch_mod=Rayleigh_channel(modulated).rayleigh_ch()
demod=MQAM_demodulate(rch_mod,m)
x=(demod.demodulate())
err=0
for x,y in zip(mod.forber,demod.uni_mod):
    if(x!=y):
        err+=1
print(err/len(mod.forber))