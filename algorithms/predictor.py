import redis
import scipy.sparse
from json import loads, dumps
from saving import load_sparse_csr, unpickle
import MySQLdb as mdb
import numpy as np
from secret import pw
import time

cache = {}

def recommendations(username):
	if username in cache:
		return cache[username]
	else:
		db = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8')
		
		with db:    
			cur = db.cursor()
			cur.execute("SELECT pattern_id FROM Projects WHERE username = %s AND pattern_id IS NOT Null;", (username,))
			projects = [int(row[0]) for row in cur]
		
		user_projects = [pattern_translate[project] for project in projects if project in trained_patterns]
		prediction = predictor[user_projects].sum(axis=0)
		prediction = scipy.sparse.csr_matrix(prediction)
		
		model_prediction = np.argsort(prediction.data)[::-1]
		model_prediction = prediction.indices[model_prediction]
		model_ranks = [pattern_tran_reverse[pattern] for pattern in model_prediction]
		model_set = set(model_ranks)
		popularity_prediction = [p for p in pop_ranks if p not in model_set]
		model_ranks.extend(popularity_prediction)
		cache[username] = model_ranks
		
		return model_ranks
    
def top_five(ranks, craft, category, L=5):
	recommendations = []
	for pattern_id in ranks:
		if pattern_id in crafts and pattern_id in categories:
			if crafts[pattern_id] == craft and categories[pattern_id] == category:
				recommendations.append(pattern_id)
		if len(recommendations) >= L: break
	return recommendations
    

def run():
    q = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')

    while True:
        args = loads(q.blpop("tasks")[1].decode('utf-8'))
        recs = recommendations(args[0])
        patterns = top_five(recs, args[1], args[2])
        q.rpush("results", dumps(patterns))

if __name__ == "__main__":
    predictor = load_sparse_csr('data/predictor.npz')
    pattern_translate = unpickle('data/pattern_translate')
    pattern_tran_reverse = unpickle('data/pattern_tran_reverse')
    popularity = unpickle('data/popularity')
    pop_ranks = sorted(popularity, key = popularity.get, reverse=False)
    trained_patterns = set(unpickle('data/trained_on_patterns'))
    crafts = unpickle('data/crafts')
    categories = unpickle('data/categories')
    run()
