import MySQLdb as mdb
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import math
import scipy.sparse
import random
from scipy.sparse import coo_matrix
import pickle

from secret import pw

con = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8');
pattern_df = pd.read_sql("SELECT pattern_id, craft_id, categories FROM Patterns;", con)
con.close()

fh = open('trained_on_patterns', 'r')
trained_patterns = pickle.load(fh)
fh.close()

fh = open('user_ranks_dict', 'r')
user_ranks_dict = pickle.load(fh)
fh.close()

pattern_library = {k : g['pattern_id'].tolist() for k, g in pattern_df.groupby('craft_id')}

knit_patterns = list(set(trained_patterns).intersection(set(pattern_library[2])))
crochet_patterns = list(set(trained_patterns).intersection(set(pattern_library[1])))

user_knit_ranks = {}
for user in user_ranks_dict:
	user_knit_ranks[user] = {pattern : user_ranks_dict[user][pattern] for pattern in user_ranks_dict[user] if pattern in knit_patterns} 

user_crochet_ranks = {}
for user in user_ranks_dict:
	user_crochet_ranks[user] = {pattern : user_ranks_dict[user][pattern] for pattern in user_ranks_dict[user] if pattern in crochet_patterns}


def scores(user, L=10):
	n = len(user_totest_dict[user])
	user_ranks = user_crochet_ranks[user]
	m = 0.0
	p = 0.0
	for rank_pair in user_ranks:
		if user_ranks[rank_pair][0] <= L: m = m + 1
		if user_ranks[rank_pair][1] <= L: p = p + 1
	return n, m/n, p/n

general_knit_scores = {}
for user in user_knit_ranks:
	general_knit_scores[user] = scores(user, L=50)

knit_project_numbers = []

for user in general_knit_scores:
	knit_project_numbers.append(general_knit_scores[user][0])

knit_project_numbers_avg = list(set(knit_project_numbers))
knit_popularity_score_avg = []
knit_model_score_avg = []

for number in knit_project_numbers_avg:
	number_model = []
	number_popularity = []
	for user in general_knit_scores:
		if general_knit_scores[user][0] == number:
			number_model.append(general_knit_scores[user][1])
			number_popularity.append(general_knit_scores[user][2])
	knit_model_score_avg.append(np.mean(number_model))	
	knit_popularity_score_avg.append(np.mean(number_popularity))	
	
plt.scatter(knit_project_numbers_avg, knit_model_score_avg)
plt.scatter(knit_project_numbers_avg, knit_popularity_score_avg, color='red')
plt.xlabel('Number of projects done')
plt.title('Knitting recommendation score')


general_crochet_scores = {}
for user in user_crochet_ranks:
	general_crochet_scores[user] = scores(user, L=50)

crochet_project_numbers = []

for user in general_crochet_scores:
	crochet_project_numbers.append(general_crochet_scores[user][0])

crochet_project_numbers_avg = list(set(crochet_project_numbers))
crochet_popularity_score_avg = []
crochet_model_score_avg = []

for number in crochet_project_numbers_avg:
	number_model = []
	number_popularity = []
	for user in general_crochet_scores:
		if general_crochet_scores[user][0] == number:
			number_model.append(general_crochet_scores[user][1])
			number_popularity.append(general_crochet_scores[user][2])
	crochet_model_score_avg.append(np.mean(number_model))	
	crochet_popularity_score_avg.append(np.mean(number_popularity))	
	
plt.scatter(crochet_project_numbers_avg, crochet_model_score_avg)
plt.scatter(crochet_project_numbers_avg, crochet_popularity_score_avg, color='red')
plt.xlabel('Number of projects done')
plt.title('Crocheting recommendation score')




