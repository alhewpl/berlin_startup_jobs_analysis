import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
import datetime


user_agent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'}

allJobLink = []
allJobsAd = []

for i in range(1,20):
    page = "http://berlinstartupjobs.com/engineering/page/{0}".format(i)
    response  = requests.get(page, headers = user_agent)

    soup = BeautifulSoup(response.content,'html.parser')

#Get all jobs list
    allJobsList = soup.find_all("div", class_="post")

#Get the links to access each job full description

    for job in allJobsList:
        job = job.find("h2", class_="product-listing-h2").find("a")['href']
        allJobLink.append(job)
        

#Grab full content from the links 
    for link in allJobLink:
        response =  requests.get(link, headers = user_agent)
        jobSoup = BeautifulSoup(response.content, 'html.parser')

        allJobsListeach = jobSoup.find_all("div", class_="w-col w-col-8")



#Get company name, Job Title, Small Description and Long Description 
        

        for job in allJobsListeach:
            companyName = job.find('span', class_='title-company-name')
            anchor= companyName.text.split("// ")[1]

            jobTitle = job.find("h1", class_="bsj-h1").get_text()
            justIt = jobTitle.split("//")[0]

            job_small_description_tag = job.find('div', class_= 'paragraph')
            job_small_description = job_small_description_tag.get_text()

            job_long_description_tag = job.find('div', class_= 'white-bg')
            job_long_description = job_long_description_tag.get_text()

#Create the dictionnary

            jobAd = { 'companyName': anchor, 'jobTitle': justIt, 'jobDescriptipnShort': job_small_description, 
            'jobDescriptipnLong': job_long_description}

            allJobsAd.append(jobAd)

   


#Move content to database            
conn = sqlite3.connect('/Users/ograndberry/documents/frauenloop/Data_science_project_1/berlin_startup_jobs_analysis/sof_db')


for jobAd in allJobsAd:
    
    c = conn.cursor()
    qu = "('{0}','{1}','{2}','{3}','{4}')".format(jobAd['companyName'], jobAd['jobTitle'],jobAd['jobDescriptipnLong'].strip(), datetime.date.today() ,'Berlin Startup Jobs')
    c.execute("INSERT INTO raw_data_bsj(Company_name,Jobtitle,Description,Date,Source) VALUES {0}".format(qu))

    
conn.commit()
conn.close()



