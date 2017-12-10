import feedparser
import sqlite3
import datetime
import re
from bs4 import BeautifulSoup  # Or from BeautifulSoup import BeautifulSoup


conn = sqlite3.connect('/Users/alina/Desktop/StartupJobs/BerlinStartupJobsAnalysis', timeout=1)
d = feedparser.parse('https://stackoverflow.com/jobs/feed?location=berlin')



for entry in d['entries']:
	if 'tags' not in entry:
		continue
	tags = entry['tags']
	title = entry['title']
	soup = BeautifulSoup(entry['description'])
	description = soup.get_text()
	company = entry['author']

	c = conn.cursor()
	#print(title)

	c.execute("INSERT INTO Stackoverflow_jobs_12_june(jobtitle, description, company_name, Date, source) VALUES (?,?,?,?,?)",(title, description, company, datetime.date.today(), 'Stackoverflow'))
	jobid = c.lastrowid

	for tag in tags:
		term = tag['term']
		#print(term)
		c.execute("INSERT INTO Skills_12_june(skill, job_id) VALUES (?,?)",(term, jobid))



conn.commit()
conn.close()





