# -*- coding: utf-8 -*-
"""Untitled26.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U268a9b_zRGNBPb3eecLnaFZRZYFyOOS
"""

!pip install -U spacy

!pip install textwrap3

!python -m spacy download en_core_web_lg

!python -m spacy validate

import spacy
from collections import Counter
from string import punctuation
import en_core_web_lg

nlp = en_core_web_lg.load()

def top_sentence(text, limit=2):
    keyword = []

    #POS tags we are interested in
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']

    #convert to lower case
    doc = nlp(text.lower())

    #iterate through tokens
    for token in doc:

        #strip out stop words and punctuations
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        
        #if then token's POS is in the list we are interested in, store the hold in list
        if(token.pos_ in pos_tag):
            keyword.append(token.text)

    #get frequency of each word
    freq_word = Counter(keyword)

    #get maximum frequency across all words in the document
    max_freq = Counter(keyword).most_common(1)[0][1]

    #normalize frequency of each word by dividing it by max frequency
    for w in freq_word:
        freq_word[w] = (freq_word[w]/max_freq)

    #calculate the strength of each sentence using the frequency of each word in that sentence
    sentence_strength={}
    for sent in doc.sents:
      for word in sent:
        if word.text in freq_word.keys():
          if sent in sentence_strength.keys():
            sentence_strength[sent]+=freq_word[word.text]
          else:
            sentence_strength[sent]=freq_word[word.text]
        
    #sort sentences basis their strength
    sorted_by_strength_sentences = sorted(sentence_strength.items(), key=lambda kv: kv[1], reverse=True)

    #create a summary basis the number of top 'k' sentences to be picked
    summary=[]
    for i in range(len(sorted_by_strength_sentences)):
      if (i<limit):
        txt = str(sorted_by_strength_sentences[i][0])
        summary.append(txt.capitalize())
      i+=1
    
    return ' '.join(summary)

input ='A lot of organizations, even in current world of the cloud and offered services, opt for their own managed instance of database. And at certain point in time (during development, testing orproduction), with increase in the read/write operations on database, they start experiencing the degraded performance. Even, the best chosen configuration, a high end virtual machine and disk on cloud has some restriction on the amount of IOPS and throughput that can be performed and is directly related to the performance of the database.'
summary = top_sentence(input, limit=2)

from textwrap3 import wrap

print (input)
print ('-------')
print (summary)

