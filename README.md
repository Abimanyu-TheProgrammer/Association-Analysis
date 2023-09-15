# Overview
This repository stores the Python code, Data, and Paper for Association Analysis of Wikidata Properties, a project for Introduction to Artificial Intelligence and Data Science (AIDS) course.

## Required Modules
- mlxtend
- apyori
- pandas
- numpy
- tqdm
- SPARQLWrapper
- json
- rdflib
- csv

## Description of files
- The .json files are filled with 100 entities and were downloaded from Wikidata.
- The .nt and .txt files are the result of AIDS_N_triples.py
- N_triples.py file converts .json files to .nt (and .txt files) and filters out external properties of the entities based on the external_prop.csv.
  These .nt files are then stored in an Apache Jena Fuseki server to make querying faster for processing, as it is stored in a local server.
- Processing.py processes the data stored to be used in the FP-Growth Algorithm.
- Association Analysis.pdf file is the result of the analysis.
