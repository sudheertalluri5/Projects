# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 19:18:20 2019

@author: sudhe
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 18:59:09 2019

@author: sudhe
"""
import sys
import pandas as pd

try:
    df=pd.read_csv(input("Enter the csv file location:"))
    #df=df.select_dtypes(exclude=[object])
    df.dropna()
except Exception as e:
    print(e)
    sys.exit("Enter a valid csv")
try:
    arff_file=input("Enter the path including filename.arff: ")
except Exception as e:
    print(e)
    sys.exit()
file_name=arff_file.split("/")[-1]
result=""

result+=("@relation "+file_name.split(".")[0]+"\n")

attributes=list(df.columns)
data_types=list(df.dtypes)
#data=[[] for i in range(df.shape[0])]
for i,attribute in enumerate(attributes):
    print(attribute)
    result+=("@attribute "+attribute+" ")
    if('int' in str(data_types[i])):
        result+=("NUMERIC"+"\n")
    elif ('float' in str(data_types[i])):
        result+="REAL"
    else:
        result+="{"+",".join(list(map(str,set(df[attribute]))))+"}\n"
    print("done")
data=list(map(list, df.itertuples(index=False)))
result+=("@data\n")
for d in data:
    result+=",".join(map(str,d))+"\n"

with open(arff_file,'w') as arfffile:
    arfffile.write(result)    