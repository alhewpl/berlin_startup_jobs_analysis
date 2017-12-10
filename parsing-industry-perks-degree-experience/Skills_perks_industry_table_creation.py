
# coding: utf-8

# # NLTK application

# **1. Imports and databse connection**

# In[1]:


import nltk
import sqlite3
import pandas as pd
import string
import regex as re 

import warnings
warnings.filterwarnings('ignore')

from nltk.tokenize import TweetTokenizer
from nltk.tokenize import MWETokenizer
from nltk.corpus import stopwords

conn = sqlite3.connect('/Users/ograndberry/Desktop/berlin_startup_jobs_analysis/bsj_db.db')
c = conn.cursor()


# **2. Get the raw data**

# In[2]:


raw_data = pd.read_sql_query('SELECT * FROM bsj_table',conn)
raw_data.head()


# **3. Import the perks, skills, and industry csv files**

# In[3]:


skills_rawdata= pd.read_csv('Skills.csv')
perks_rawdata= pd.read_csv('Perks.csv')
industry_rawdata = pd.read_csv('Industry.csv')


# In[4]:


skills_rawdata.head()


# **Reshape the tables**

# In[5]:


#reshape to 2 to rows 
skills_rawdata = pd.melt(skills_rawdata, id_vars=['group'])
#drop null values
skills_rawdata.dropna(inplace=True)
#drop unecessary columns
skills_rawdata.drop('variable',1, inplace=True)
#make the text lower
skills_rawdata['group'] = skills_rawdata['group'].str.lower()
skills_rawdata['value'] = skills_rawdata['value'].str.lower()


# In[6]:


perks_rawdata = pd.melt(perks_rawdata, id_vars=['group'])
perks_rawdata.dropna(inplace=True)
perks_rawdata.drop('variable',1, inplace=True)
perks_rawdata['group'] = perks_rawdata['group'].str.lower()
perks_rawdata['value'] = perks_rawdata['value'].str.lower()


# In[7]:


industry_rawdata = pd.melt(industry_rawdata, id_vars=['group'])
industry_rawdata.dropna(inplace=True)
industry_rawdata.drop('variable',1, inplace=True)
industry_rawdata['group'] = industry_rawdata['group'].str.lower()
industry_rawdata['value'] = industry_rawdata['value'].str.lower()


# In[8]:


#check an example outcome
skills_rawdata.head()


# **4. Create list of keywords for each category**

# In[9]:


#empty list to save the 3 following lists in it
all_list = []
skills_list = skills_rawdata['value'].str.lower().str.split().tolist()
perks_list = perks_rawdata['value'].str.lower().str.split().tolist()
industry_list = industry_rawdata['value'].str.lower().str.split().tolist()

#join all lists 
all_list.extend(skills_list)
all_list.extend(perks_list)
all_list.extend(industry_list)


# In[10]:


#at this stage we have all keywords we saved as import to grab if present of in the job description
all_list


# **5. Use the list to tockenize the job descriptions**

# In[11]:


tokenizer = MWETokenizer()
tknzr = TweetTokenizer()


# In[12]:


def text_process_group(mess):
    """
    1. Lower case the input
    2. Remove punctuation expect '-'
    3. Apply custom tokenizer
    4. Return column of clean text words"""
    mess.lower()
    regex = r"[^\P{P}-]+"
    new_mess= re.sub(regex, " ", mess, 0)    
    tokenizer = MWETokenizer(all_list, separator=' ')
    token = tokenizer.tokenize(new_mess.lower().split())
    sw = [x for x in token if x not in stopwords.words('english')]
    return sw


# In[13]:


#apply the customized tokenizer, it takes a bit more time
raw_data['description 2'] = raw_data['description'].apply(text_process_group)


# In[14]:


raw_data.head()


# **6. Create clusters**

# In[15]:


#create dictionnaries of keyords and their respective clusters
skills_model = skills_rawdata.set_index('value').to_dict()['group']
perks_model = perks_rawdata.set_index('value').to_dict()['group']
industry_model = industry_rawdata.set_index('value').to_dict()['group']


# In[16]:


skills_model


# **7. Apply cluster to harmonize**

# In[17]:


skills_tagger = nltk.tag.UnigramTagger(model=skills_model)
perks_tagger = nltk.tag.UnigramTagger(model=perks_model)
industry_tagger = nltk.tag.UnigramTagger(model=industry_model)


# In[18]:


#create new tables with the id and the description 2
skills_table = raw_data[['id','description 2']]
perks_table = raw_data[['id','description 2']]
industry_table = raw_data[['id','description 2']]


# In[19]:


#create the tagging fuction 
def applytagskills(word):
    tag= skills_tagger.tag(word)
    return tag

def applytagperks(word):
    tag= perks_tagger.tag(word)
    return tag

def applytagindustry(word):
    tag= industry_tagger.tag(word)
    return tag


# In[20]:


#apply the tagging fuction
skills_table['tags']= skills_table['description 2'].apply(applytagskills)
perks_table['tags'] = perks_table['description 2'].apply(applytagperks)
industry_table['tags'] = industry_table['description 2'].apply(applytagindustry)


# In[21]:


skills_table.head()


# **8. Clean the final tables**

# In[22]:


skills_table = skills_table.set_index(['id'])['tags'].apply(pd.Series).stack()
skills_table = pd.DataFrame(skills_table.reset_index(level=1, drop=True))
skills_table.columns = ['combinaisons']
skills_table.index.names = ['job_id']
#split tuples into 2 columns
skills_table = skills_table ['combinaisons'].apply(pd.Series)
#rename column
skills_table.columns = ['words','skill_name']
skills_table.dropna(inplace = True)
skills_table.reset_index(inplace = True)
#when a job ad muliple keywords leading to the same category we need to avoid repetition
skills_table = skills_table.drop_duplicates(['job_id','skill_name']).set_index('job_id')
skills = skills_table[['skill_name']]


# In[23]:


perks_table = perks_table.set_index(['id'])['tags'].apply(pd.Series).stack()
perks_table= pd.DataFrame(perks_table.reset_index(level=1, drop=True))
perks_table.columns = ['combinaisons']
perks_table.index.names = ['job_id']
#split tuples into 2 columns
perks_table= perks_table['combinaisons'].apply(pd.Series)
#rename column
perks_table.columns = ['words','perk_name']
perks_table.dropna(inplace = True)
perks_table.reset_index(inplace = True)
#when a job ad muliple keywords leading to the same category we need to avoid repetition
perks_table = perks_table.drop_duplicates(['job_id','perk_name']).set_index('job_id')
perks = perks_table[['perk_name']]


# In[24]:


industry_table = industry_table .set_index(['id'])['tags'].apply(pd.Series).stack()
industry_table = pd.DataFrame(industry_table.reset_index(level=1, drop=True))
industry_table .columns = ['combinaisons']
industry_table .index.names = ['job_id']
#split tuples into 2 columns
industry_table = industry_table ['combinaisons'].apply(pd.Series)
#rename column
industry_table .columns = ['words','industry_name']
industry_table .dropna(inplace = True)
industry_table .reset_index(inplace = True)
#when a job ad muliple keywords leading to the same category we need to avoid repetition
industry_table  = industry_table .drop_duplicates(['job_id','industry_name']).set_index('job_id')
industry = industry_table [['industry_name']]


# In[25]:


skills.head()


# In[26]:


industry.head()


# In[27]:


perks.head()


# **9. Send the tables to the database**

# In[28]:


skills.to_sql('Skills', conn, if_exists='replace')
perks.to_sql('Perks', conn, if_exists='replace')
industry.to_sql('Industry', conn, if_exists='replace')

