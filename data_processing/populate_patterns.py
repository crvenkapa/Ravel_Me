import MySQLdb as mdb
import csv
import sys
import json
import datetime
import os

from secret import pw

def convert(x):
	if x:
		if x.isdigit():
			return int(x)
		else:
			a,b = x.split('-')
			return (int(a) + int(b))/2 


csv.field_size_limit(sys.maxsize)

con = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8');

c = con.cursor()

filenames = os.listdir('data')

for filename in filenames:
	if 'pattern_directory' in filename:
		print(filename)
		with open(os.path.join('data', filename), 'r') as fh:
			csvreader = csv.reader(fh)
			for line in csvreader:
				try:
					pattern = json.loads(line[1])['pattern']
				except ValueError:
					continue
				pattern['pattern_id'] = int(line[0])
				pattern['craft_id'] = pattern['craft']['id']
				if pattern['photos']:
					pattern['photo_url'] = pattern['photos'][0]['small_url']
				else:
					pattern['photo_url'] = None
				
				if pattern['published']:
					pattern['date'] = datetime.datetime.strptime(pattern['published'], '%Y/%m/%d')
				else: pattern['date'] = None 
				
				if 'yarn_weight' in pattern:
					pattern['knit_gauge'] = convert(pattern['yarn_weight']['knit_gauge'])
					pattern['weight_name'] = pattern['yarn_weight']['name']
					pattern['ply'] = convert(pattern['yarn_weight']['ply'])
					pattern['wpi'] = convert(pattern['yarn_weight']['wpi'])
				else:
					pattern['knit_gauge'] = None
					pattern['weight_name'] = None
					pattern['ply'] = None
					pattern['wpi'] = None
				
				if pattern['pattern_categories']:
					p = pattern['pattern_categories'][0]
					s = p['name']
					while 'parent' in p and p['parent']['name'] != 'Categories':
						p = p['parent']
						s = p['name'] + ',' + s	
					pattern['categories'] = s
				else:
					pattern['categories'] = None	
				
				c.execute('INSERT INTO Patterns VALUES(%(pattern_id)s, %(name)s, %(comments_count)s, %(craft_id)s, ' \
					'%(difficulty_average)s, %(difficulty_count)s, %(downloadable)s, %(favorites_count)s, %(free)s, ' \
					'%(yardage)s, %(yardage_max)s, %(projects_count)s, %(queued_projects_count)s, %(rating_average)s,' \
					'%(rating_count)s, %(ravelry_download)s, %(knit_gauge)s, %(weight_name)s, %(ply)s, %(wpi)s, ' \
					'%(categories)s, %(date)s)', pattern)

		con.commit()

fh.close()
c.close()
con.close()
