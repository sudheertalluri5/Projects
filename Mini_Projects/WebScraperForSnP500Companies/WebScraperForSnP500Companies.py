import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
page=urlopen(url)

soup=bs(page)

table=soup.findAll("table",{"id":"constituents"})

for t in table:
    rows=(t.find_all("tr"))
    row_list=list()
    for row in rows:
        data_list=(row.find_all("td"))
        temp=tuple()
        for data in data_list:
            temp+=(data.text,)
        if(len(temp)!=0):
            row_list.append(temp)
    #print(row_list)
    headings=t.find_all("th")
    head_tuple=tuple()
    for heading in headings:
        head_tuple+=(heading.text,)
df=pd.DataFrame(row_list,columns=head_tuple)
df.head(10)