import nltk
import csv, codecs 
import numpy as np
from nltk.corpus import stopwords 
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.tag.perceptron import PerceptronTagger  

processed_word_list = {}

reader = codecs.open('raw_data.csv', 'r', errors="ignore") 
for line in reader:
        if line not in stopwords.words('english'): 
            line = line.lower() 
            tokens = word_tokenize(line) 
            #posData = pos_tag(tokens) 
            #print(posData)
            #processed_word_list.append(posData)
            #print(processed_word_list)
            

        model = {'Rails': 'ror','ruby on rails': 'ror', 'Ruby': 'ror'}
        tagger = nltk.tag.UnigramTagger(model=model)

        print(tagger.tag(tokens))            