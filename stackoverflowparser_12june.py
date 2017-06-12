import feedparser
import sqlite3

conn = sqlite3.connect('/Users/alina/Documents/BerlinStartupJobsAnalysis', timeout=1)
d = feedparser.parse('https://stackoverflow.com/jobs/feed?location=berlin')


for entry in d['entries']:
	if 'tags' not in entry:
		continue
	tags = entry['tags']
	title = entry['title']
	description = entry['description']
	company = entry['author']
	c = conn.cursor()
	#print(title)
	c.execute("INSERT INTO Stackoverflow_jobs_12_june(Jobtitle, Description, Company_name) VALUES (?,?,?)",(title, description, company))
	jobid = c.lastrowid

	for tag in tags:
		term = tag['term']
		print(term)
		c.execute("INSERT INTO Skills_12_june(skill_name, job_id) VALUES (?,?)",(term, jobid))



	
#print('\n')
	# company = entry['author']
	# summary = entry['summary']
	# experience_required = False if summary.find('years') == -1 else True




conn.commit()
conn.close()





