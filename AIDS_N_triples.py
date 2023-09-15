#!/usr/bin/env python
# coding: utf-8

# In[74]:


import json
from rdflib import Graph, URIRef
from csv import reader
from tqdm import tqdm
import pandas as pd


# In[75]:


import chardet
with open('song100.json', 'rb') as rawdata:
    result = chardet.detect(rawdata.read(1000000))
result


# In[76]:


extCSV = pd.read_csv('external_prop.csv')
extProp = extCSV['external_properties'].tolist()


# In[77]:


f = open('song100.json', encoding='utf8') 


# In[78]:


data = json.load(f)


# In[79]:


data[0]


# In[80]:


data[0]['p'].split('/')[-1]


# In[81]:


data[0]['o']


# In[82]:


'<'+data[0]['s']+'> <' + data[0]['p'] + '> <' + data[0]['o'] + '>'


# In[83]:


for i, j in data[0].items():
    print(j)


# In[84]:


f = open("song.nt", "w")
fr = open("song.txt", 'w')


# In[85]:


for i in tqdm(range(len(data))):
    s = data[i]['s']
    p = data[i]['p']
    o = data[i]['o']
    propRaw = p.split('/')
    prop = propRaw[-1]
    if prop in extProp:
        continue
    if 'http://www.wikidata.org/entity/' not in o:
        o = "\"\"@en ."
        triple = '<'+ s +'> <' + p + '> ' + o
        f.write(triple + "\n")
        fr.write(triple + "\n")
        continue
    triple = '<'+ s +'> <' + p + '> <' + o + '> .'
    f.write(triple + "\n")
    fr.write(triple + "\n")

