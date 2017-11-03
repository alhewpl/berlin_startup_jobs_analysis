import json
import csv
import sqlite3

data = []
with open('BSJ-Tech-Skills.csv', 'r', encoding="utf-8") as file:
    for row in csv.DictReader(file):
        data.append(row)

json_data = json.dumps(data)
output_file=open('test.json', 'w')
output_file.write(json_data)
output_file.close()

contents = open('test.json', "r").read() 
for item in contents.strip().split('\n'):
    data2 = json.loads(str(item))


skills = {d['Jobtitle-id']: d['Skill'].split(',') for d in data2} 

conn = sqlite3.connect('/Users/alina/Desktop/webscraping/berlinstartupjob/anothertry')

for i,v in skills.items():
    for v1 in v:
        #print (v)
        c = conn.cursor()
        c.execute("INSERT INTO bsj_skills(jobid, skill) VALUES (?,?)",(int(i), str(v1)))

conn.commit()
conn.close()        

