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

	# Makes subplots:
	fig = plt.figure()
	fig.patch.set_alpha(0)
	ax1 = fig.add_subplot(2,1,2)

	ind = np.array([1,2])
	width = 0.5
	ax1.bar(ind, model_v_popularity, width)
	ax1.xaxis.set_ticks([1.25, 2.25])
	ax1.xaxis.set_ticklabels(['Personalized Accuracy', 'Popularity Accuracy'])
	ax1.set_xlim([0.75,2.75])
	ax1.set_title('Percentage of Test Ranks in Top 0.02%')

	ax2 = fig.add_subplot(2,1,1)
	ax2.barh(0.25, m2/total1, height=0.5, left=0)
	ax2.barh(0.25, p2/total1, height=0.5, left=m2/total1, color='g')
	ax2.set_ylim([0,1])
	ax2.yaxis.set_ticks([])
	ax2.set_title('Percentage of Higher Ranking Test Ranks')

	fig.savefig('val.png', facecolor=fig.get_facecolor())



