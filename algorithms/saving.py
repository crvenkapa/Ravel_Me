import numpy as np
from scipy.sparse import csr_matrix
import pickle

def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

def save_item(filename, item):
	fh = open(filename, 'w')
	pickle.dump(item, fh)
	fh.close()
	
def unpickle(filename):
	fh = open(filename, 'r')
	result = pickle.load(fh)
	fh.close()
	return result

