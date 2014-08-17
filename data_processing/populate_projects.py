import MySQLdb as mdb
import csv
import sys
import json
from datetime import datetime
import os
from secret import pw

csv.field_size_limit(sys.maxsize)

con = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8');

c = con.cursor()

filenames = os.listdir('data')

fh3 = open('user_errors', 'w')
csvmissed = csv.writer(fh3)

for filename in filenames:
	if 'projects_batch' in filename:
		print(filename)
		with open(os.path.join('data', filename), 'r') as fh:
			csvreader = csv.reader(fh)
			for line in csvreader:
				try:
					projects = json.loads(line[2])		
					for project in projects['projects']:
						project['username'] = line[1]
						if project['started']:
							project['started'] = datetime.strptime(project['started'], '%Y/%m/%d')
						if project['completed']:
							project['completed'] = datetime.strptime(project['completed'], '%Y/%m/%d')
						if project['started'] and project['completed']:
							project['days'] = abs(project['completed'] - project['started']).days
						project['created_at'] = datetime.strptime(project['created_at'][:10], '%Y/%m/%d')
						if 'tag_names' in project:
							project['tag_names'] = ','.join(project['tag_names'])
						c.execute('INSERT INTO Projects VALUES(%(user_id)s, %(username)s, %(pattern_name)s, %(pattern_id)s, %(status_name)s, ' \
							'%(started)s, %(completed)s, %(tag_names)s, %(favorites_count)s, %(photos_count)s, %(comments_count)s, ' \
							'%(craft_id)s, %(created_at)s, %(made_for)s, %(progress)s, %(rating)s, %(days)s)', project)
				except:
					csvmissed.writerow(line)	
		con.commit()

fh3.close()
c.close()
con.close()

