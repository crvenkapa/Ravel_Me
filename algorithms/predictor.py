import redis
from json import loads, dumps
from saving import load_sparse_csr, unpickle
import MySQLdb as mdb
import numpy as np
from secret import pw

def recommendations(username, craft):
    db = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8')
    with db:    
        cur = db.cursor()
        cur.execute("SELECT pattern_id FROM Projects WHERE username = %s AND pattern_id IS NOT Null;", (username,))
        projects = [int(row[0]) for row in cur]
        
    user_projects = [pattern_translate[project] for project in projects if project in trained_patterns]
    prediction = sum([predictor[project,:] for project in user_projects])
    
    ordered = np.argsort(np.squeeze(prediction.toarray()))[::-1]
    
    ordered = [pattern_tran_reverse[pattern] for pattern in ordered]
    
    if craft == 'knit':
        knitting_predictions = [pattern for pattern in ordered if pattern in knitting_patterns]
        knitting_recs = [pattern for pattern in knitting_predictions if pattern not in projects]
        return knitting_recs[:5]
        
    if craft == 'crochet':
        crocheting_predictions = [pattern for pattern in ordered if pattern in crocheting_patterns] 
        crocheting_recs = [pattern for pattern in crocheting_predictions if pattern not in projects]
        return crocheting_recs[:5]


def run():
    q = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')

    while True:
        args = loads(q.blpop("tasks")[1].decode('utf-8'))
        recs = recommendations(*args)
        q.rpush("results", dumps(recs))

if __name__=="__main__":
    predictor = load_sparse_csr('predictor.npz')
    pattern_translate = unpickle('pattern_translate')
    pattern_tran_reverse = unpickle('pattern_tran_reverse')
    trained_patterns = set(unpickle('trained_on_patterns'))
    knitting_patterns = set(unpickle('knitting_patterns'))
    crocheting_patterns = set(unpickle('crocheting_patterns'))
    run()
