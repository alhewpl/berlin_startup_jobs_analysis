import nltk
import sqlite3
import pandas as pd
conn = sqlite3.connect('/Users/ograndberry/Desktop/berlin_startup_jobs_analysis/bsj_db.db')
c = conn.cursor()

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
# import nltk.tag, nltk.data
from nltk.tag.perceptron import PerceptronTagger
# from nltk.data import find
nltk.download('averaged_perceptron_tagger')
tknzr = TweetTokenizer()

class BackoffTagger:
    def __init__(self):
        self._taggers = [PerceptronTagger()]

#create variables
processed_word_list = []
text = []
ids = []
x_results = []
results = []

#imitate the list of job decriptions
#text = ['Hello how are you ruby html','ruby how are you','Hello how are you ',
#'Hello how are you ruby','Hello how are you ruby']

#imitate the list of ids corresponding to the job descriptions
#ids = [0,1,2,3,4]

#un comment below to get the real dataset
for row in c.execute("SELECT * FROM bsj_table"):
		text.append(row[3])
		ids.append(row[0])


#tokenize the text remove stop word and save the result in the variable called 'results'
for x in text:
	x_results = []
	for w in tknzr.tokenize(x):
		if w not in stopwords.words('english'):
			w = w.lower()
			x_results.append(w)
	results.append(x_results)		

#create a dictionary wih corresponding ids and tokenized text
dictionary = dict(zip(ids, results))


# Dictionary containing tags
model = {'rails': 'ror','ruby on rails': 'ror', 'ruby': 'ror','html': 'html','html5': 'html', 'html 5': 'html'}

tagger = nltk.tag.UnigramTagger(model=model)


#empty variable to stock the tagging result 
final = []
for key, values in dictionary.items():
	final.append(tagger.tag(values))



#empty variable to stock unique tag
a = []
for x in final:
	a.append([c[1] for c in x if c[1]!=None])



#create dictionary with corresponding ids and unique tag
dic = dict(zip(ids,a))


#create list to stock the corresponding tuples (id and tag)
cc =[]
for k, v in dic.items():
	for e in v:
		cc.append((k,e))


#export to database
for x, y in cc:
	c.execute("INSERT INTO Skills(skill_name, job_id) VALUES (?,?)",(y, x))


conn.commit()
conn.close()


