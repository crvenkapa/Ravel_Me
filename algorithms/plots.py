import matplotlib.pylab as plt
import numpy as np

from saving import unpickle


def scores(user_ranks, L=50):
	m = 0.0
	p = 0.0
	q1 = 0.0
	q2 = 0.0
	n = 0
	for user in user_ranks:	
		for rank_pair in user_ranks[user]:
			n = n + 1
			if user_ranks[user][rank_pair][0] <= L:
				m = m + 1
			if user_ranks[user][rank_pair][1] <= L:
				p = p + 1
			if user_ranks[user][rank_pair][0] < user_ranks[user][rank_pair][1]:
				q1 = q1 + 1
			if user_ranks[user][rank_pair][0] >= user_ranks[user][rank_pair][1]:
				q2 = q2 + 1
	return n, m, p, q1, q2

if __name__ == "__main__":
	test_users = unpickle('../user_ranks_dict')
	total1, m1, p1, m2, p2 = scores(test_users)
	model_v_popularity = (m1/total1, p1/total1)
	m_v_p_top2 = (m2/total1, p2/total1)
	ind = np.array([1,2])
	width = 0.5
	bar1 = plt.bar(ind, m_v_p_top2, width)
	bar2 = plt.bar(ind, model_v_popularity, width, color='g')
	plt.xlim([0.75,2.75])
	plt.ylim([0,.65])
	plt.xticks(ind+width/2., ('Model Accuracy', 'Popularity Accuracy'))
	plt.legend( (p1[0], p2[0]), ('Percentage of ranks in top 0.02%', 'Winning percentage'))
