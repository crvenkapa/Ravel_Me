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

def recommendations(username, craft):
	db = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8')
	with db:	
		cur = db.cursor()
		cur.execute("SELECT pattern_id FROM Projects WHERE username = %s;", (username,))
		projects = [int(row[0]) for row in cur]
	
	#fh = open('pattern_translate', 'r')
	#pattern_translate = pickle.load(fh)
	#fh.close()
#
	#fh = open('pattern_tran_reverse', 'r')
	#pattern_tran_reverse = pickle.load(fh)
	#fh.close()
	#
	#fh = open('trained_on_patterns', 'r')
	#trained_patterns = pickle.load(fh)
	#fh.close()
	#
	#fh = open('knitting_patterns', 'r')
	#knitting_patterns = pickle.load(fh)
	#fh.close()
	#
	#fh = open('crocheting_patterns', 'r')
	#crocheting_patterns = pickle.load(fh)
	#fh.close()
	
#	predictor = np.load('predictor_matrix.npz')

	user_projects = [pattern_translate[project] for project in projects if project in trained_patterns]
	prediction = sum([predictor[project,:] for project in user_projects])
	
	ordered = np.argsort(np.squeeze(predictions.toarray()))[::-1]
	
	ordered = [pattern_tran_reverse[pattern] for pattern in ordered]
	
	if craft == 'knit':
		knitting_predictions = [pattern for pattern in ordered if pattern in knitting_patterns]
		knitting_recs = [pattern for pattern in knitting_predictions if pattern not in projects]
		return knitting_recs[:10]

	if craft == 'crochet':
		crocheting_predictions = [pattern for pattern in ordered if pattern in crocheting_patterns]	
		crocheting_recs = [pattern for pattern in crocheting_predictions if pattern not in projects]
		return crocheting_recs[:10]
		


	

