# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:12:43 2019

@author: sudhe
"""

def isfloat(attribute):
    try:
        x=float(attribute)
        return True
    except:
        return False
import csv
try:
    csv_file=input("Enter the csv file location: ")
    with open(csv_file, 'r') as csvfile:
        csvreader=csv.reader(csvfile)
        attributes=(csvreader.__next__())
        data=list()
        for row in csvreader:
            data.append(row)
except FileNotFoundError as ffe:
    print(ffe.strerror)
except Exception as e:
    print(e)

try:
    arff_file=input("Enter the path including filename.arff: ")
except Exception as e:
    print(e)
file_name=arff_file.split("/")[-1]
result=""

result+=("@relation "+file_name.split(".")[0]+"\n")
    
for i,attribute in enumerate(attributes):
    print(attribute)
    result+=("@attribute "+attribute+" ")
    if(data[0][i].isnumeric()):
        result+=("numeric"+"\n")
    elif (isfloat(attribute)):
        result+=("real"+"\n")
    else:
        att_list=set()
        for row in data:
            att_list.add(row[i])
            result+="("+",".join(list(att_list))+")\n"
    print("done")
result+=("@data/n")
for row in data:
    result+=(",".join(row)+"\n")
with open(arff_file,'w') as arfffile:
    arfffile.write(result)    