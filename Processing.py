#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from apyori import apriori
from mlxtend.preprocessing import TransactionEncoder
from tqdm import tqdm


# In[2]:


queryString = "SELECT * WHERE { ?s ?p ?o. }"
sparql = SPARQLWrapper("http://localhost:3030/memory/sparql")
sparql.setQuery(queryString)

try :
   ret = sparql.query()
   # ret is a stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
except :
   pass


# In[3]:


sparql.setQuery("""
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT ?subject (COUNT(?prop) AS ?total) {
  
  SELECT DISTINCT ?subject ?prop
    WHERE {
    ?subject ?prop ?value .
} 

} GROUP BY ?subject
ORDER BY DESC(?total) 
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


# In[4]:


res = []
for results in results["results"]["bindings"]:
    print('%s: %s' % (results["subject"]["value"], results["total"]["value"]))
    entity = str(results["subject"]["value"]).split('/')
    res.append(entity[-1])
print('---------------------------')


# In[5]:


db = []

for i in range(len(res)):
    query_string = """
    PREFIX wd: <http://www.wikidata.org/entity/>
    SELECT DISTINCT ?human ?prop {
    VALUES ?human {wd:""" + res[i] + """}
    ?country ?prop ?value .
    }
    """

    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    results_entity = sparql.query().convert()
    propLabel = []
    for results in results_entity["results"]["bindings"]:
#         print('%s: %s' % (results["country"]["value"], results["propLabel"]["value"]))
        propLabel.append(results["prop"]["value"])
#     print('---------------------------')
    db.append(propLabel)


# In[6]:


te = TransactionEncoder()
te_ary = te.fit(db).transform(db)
df = pd.DataFrame(te_ary, columns=te.columns_)
df


# In[7]:


wikidata = SPARQLWrapper("https://query.wikidata.org/sparql")


# In[8]:


propList = df.columns.tolist()
for i in range(len(propList)):
    propList[i] = propList[i].split('/')[-1]


# In[9]:


propLabel = []

for i in tqdm(range(len(propList))):
    query_string = """
    SELECT DISTINCT ?propLabel {
      VALUES ?p {wdt:""" + propList[i] + """}
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
      ?prop wikibase:directClaim ?p .
    }
    """

    wikidata.setQuery(query_string)
    wikidata.setReturnFormat(JSON)
    results_prop = wikidata.query().convert()
    for results in results_prop["results"]["bindings"]:
#         print('%s: %s' % (results["country"]["value"], results["propLabel"]["value"]))
        propLabel.append(results["propLabel"]["value"])
#     print('---------------------------')


# In[ ]:


df.columns = propLabel


# In[ ]:


df


# In[ ]:


from mlxtend.frequent_patterns import fpgrowth

fpgrowth(df, min_support=0.8)

