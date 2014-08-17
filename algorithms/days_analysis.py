import MySQLdb as mdb
import datetime
import pandas as pd
from secret import pw
import pdb


con = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8');

#The following database has 409776 rows:

pattern_df = pd.read_sql("SELECT Projects.started, Projects.completed, Patterns.yardage, " \
							"Patterns.weight_name, Projects.user_id, Patterns.pattern_id FROM Projects " \
							"LEFT JOIN Patterns ON Projects.pattern_id = Patterns.pattern_id " \
							"WHERE started AND completed AND yardage AND weight_name " \
							"IS NOT NULL AND categories LIKE '%Pet,Clothing%';", con)
														
con.close()

translate = {'Thread' : 1, 'Cobweb' : 2, 'Lace' : 3, 'Light Fingering' : 4, 'Fingering' : 5, 
				'Sport' : 6, 'DK' : 7, 'Worsted' : 8, 'Aran' : 9, 'Bulky' : 10, 'Super Bulky' : 11, 
				'DK / Sport' : 6.5, 'Aran / Worsted' : 8.5, 'Any gauge' : 11, 'No weight specified' : None}
			
pattern_df['days'] = pd.Series(abs(pattern_df.completed - pattern_df.started).astype('timedelta64[D]'))

pattern_df.weight_name = pattern_df.weight_name.apply(lambda x : translate[x])

pattern_df.to_csv('Pet_Clothing_Projects.csv')



#groupBYpattern = pattern_df['days' != 0].groupby('pattern_id')
#groupBYpattern.mean().plot(kind = 'scatter',x='days', y='yardage')
#temp = groupBYpattern.mean()
#temp2 = temp[temp.yardage < 12000]
#temp3 = temp2[temp2.days < 3000]
#temp3.plot(kind = 'scatter', x='yardage', y='days')
#temp3.plot(kind = 'scatter', x='weight_name', y='days')

#import statsmodels.formula.api as sm
#result = sm.ols(formula = "days ~ yardage + weight_name", data = temp3).fit()
#print result.summary()

#import statsmodels.api as sm
#poisson_model = sm.GLM(y, X, family = sm.families.Poisson()).fit()
#print poisson_model.summary
#print poisson_model.summary()
