import MySQLdb as mdb
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import math
import scipy.sparse
import random
from scipy.sparse import coo_matrix

from secret import pw

# Get all the user-pattern tuples who have done between 10 and 100 projects:

con = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8');
pattern_df = pd.read_sql("SELECT Projects.user_id, pattern_id FROM Projects " \
							"LEFT JOIN (SELECT user_id, COUNT(pattern_id) AS cnt FROM Projects " \
							"WHERE pattern_id IS NOT Null GROUP BY user_id) as tmp " \
							"ON Projects.user_id = tmp.user_id WHERE pattern_id IS NOT Null " \
							"AND tmp.cnt BETWEEN 10 AND 100;", con, index_col='user_id')
con.close()

users_random = random.sample(set(pattern_df.index), int(.2*len(set(pattern_df.index))))
training_users = pattern_df.drop(users_random)
testing_users = pattern_df.loc[users_random]

# Create full dictionaries mapping users to the projects they have done and vice versa:
user_dict = {k: g['pattern_id'].tolist() for k, g in pattern_df.groupby(level=0)}
pattern_dict = {k: g.index.tolist() for k, g in pattern_df.groupby('pattern_id')}
user_totrain_dict = {k: g['pattern_id'].tolist() for k, g in training_users.groupby(level=0)}
pattern_totrain_dict = {k: g.index.tolist() for k, g in training_users.groupby('pattern_id')}
user_totest_dict = {k: g['pattern_id'].tolist() for k, g in testing_users.groupby(level=0)}

del user_dict

user_translate = {user:i for i, user in enumerate(user_totrain_dict)}
pattern_translate = {pattern: i for i, pattern in enumerate(pattern_totrain_dict)}
pattern_tran_reverse = {k : g for g, k in pattern_translate.items()}

row = training_users.index.map(lambda x : user_translate[x])
column = training_users.pattern_id.map(lambda x : pattern_translate[x])
data = np.ones(len(column))


sparse_matrix = coo_matrix((data, (row, column.values)), shape = (len(user_totrain_dict), len(pattern_totrain_dict)))
S = sparse_matrix.tocsr()

del pattern_df
del sparse_matrix

predictor = S.T.dot(S)

D = 1/np.sqrt(predictor.diagonal())
d = predictor.diagonal()
del predictor

orde = np.argsort(d)[::-1]
pop_ranks = {}
for i, patt in enumerate(orde):
	pop_ranks[pattern_tran_reverse[patt]] = i + 1

D = scipy.sparse.dia_matrix((D,[0]), (len(D),len(D)))
p = D.dot(S.T)
del S
predictor = p.dot(p.T)
del p
	
#def model_rank(user_id):
	#user_projects = [pattern_translate[project] for project in user_totest_dict[user_id] if project in pattern_totrain_dict]
	#prediction = sum([predictor[project,:] for project in user_projects])
	#rankings = {}
	#for project in user_projects:
		#pred_temp = prediction - predictor[project,:]
		#order = np.argsort(np.squeeze(pred_temp.toarray()))[::-1]
		#patt_id = pattern_tran_reverse[project]
		#rankings[patt_id] = [list(order).index(project) + 1, pop_ranks[patt_id]]
	#return rankings
#
#print('ranking users')
#
#users_totest_random = random.sample(user_totest_dict, 1000)
#
#user_ranks_dict = {}
#for user in users_totest_random:
	#user_ranks = model_rank(user)
	#user_ranks_dict[user] = user_ranks
	##user_ranks_dict[user] = [np.mean([user_ranks[project][0] for project in user_ranks]), np.mean([user_ranks[project][1] for project in user_ranks])]
#
#def scores(user, L=10):
	#n = len(user_totest_dict[user])
	#user_ranks = model_rank(user)
	#m = 0.0
	#p = 0.0
	#for rank_pair in user_ranks:
		#if user_ranks[rank_pair][0] <= L: m = m + 1
		#if user_ranks[rank_pair][1] <= L: p = p + 1
	#return n, m/n, p/n


#def predict(user_id, limit=10):
	#user_projects = [pattern_translate[project] for project in user_dict[user_id]]
	#v = np.zeros(len(pattern_dict))
	#for project in user_projects:
		#v[project] += 1
	#prediction = predictor_normalized.dot(v)
	#prediction = (1./len(user_projects))*prediction 
	#order = np.argsort(prediction)[::-1]
	#recs = [pattern_tran_reverse[i] for i in order if i not in user_projects]
	#return recs[:limit]



