import MySQLdb as mdb
import datetime
import pandas as pd
import matplotlib.pylab as plt
from secret import pw


def hexplot(user_list):
	#user_list = ",".join([str(user) for user in user_list])
	user_list = str(user_list)
	translate = {'Thread' : 1, 'Cobweb' : 2, 'Lace' : 3, 'Light Fingering' : 4, 'Fingering' : 5, 
				'Sport' : 6, 'DK' : 7, 'Worsted' : 8, 'Aran' : 9, 'Bulky' : 10, 'Super Bulky' : 11, 
				'DK / Sport' : 6.5, 'Aran / Worsted' : 8.5, 'Any gauge' : 11, 'No weight specified' : None}

	##The following dataframe consists of the user's projects (if all data was entered):
	con = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8');
	pattern_df = pd.read_sql("SELECT Projects.started, Projects.completed, Patterns.yardage, Patterns.weight_name, " \
								"Patterns.pattern_id FROM Projects " \
								"LEFT JOIN Patterns ON Projects.pattern_id = Patterns.pattern_id " \
								"WHERE user_id IN (" + user_list + ") AND started AND completed AND yardage AND weight_name " \
								"IS NOT NULL;", con)
	con.close()
	
	#Compute number of days per project and translate gauges:
	pattern_df['days'] = pd.Series(abs(pattern_df.completed - pattern_df.started).astype('timedelta64[D]'))
	pattern_df.weight_name = pattern_df.weight_name.apply(lambda x : translate[x])
	
	#temp = pattern_df[pattern_df.yardage < 6000]
	
	#Plot what we have:
	pattern_df.plot(kind = 'hexbin', x = 'yardage', y = 'weight_name', C = 'days', gridsize=50, bins = 'log')
	plt.title('User ' + user_list)	


#Users tried: 1, 69567, 69581

