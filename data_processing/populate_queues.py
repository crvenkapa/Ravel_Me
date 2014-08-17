import MySQLdb as mdb
import csv
import sys
import json
import datetime
import os
from secret import pw

csv.field_size_limit(sys.maxsize)

con = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8');

c = con.cursor()

filenames = os.listdir('data')

fh3 = open('queue_errors', 'w')
csvmissed = csv.writer(fh3)

for filename in filenames:
	if 'queues_batch' in filename:
		print(filename)
		with open(os.path.join('data', filename), 'r') as fh:
			csvreader = csv.reader(fh)
			for line in csvreader:
				try:
					queues = json.loads(line[2])
				except ValueError:
					continue			
				for queue in queues['queued_projects']:
					queue['username'] = line[1]
					queue['created_at'] = datetime.datetime.strptime(queue['created_at'][:10], '%Y/%m/%d')
					c.execute('INSERT INTO Queues VALUES(%(user_id)s, %(username)s, %(pattern_name)s, %(pattern_id)s, ' \
						'%(created_at)s, %(position_in_queue)s, %(skeins)s, %(yarn_id)s, %(yarn_name)s)', queue)
		con.commit()

fh3.close()
c.close()
con.close()
