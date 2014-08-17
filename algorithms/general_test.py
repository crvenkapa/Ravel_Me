import pickle
import matplotlib.pylab as plt

fh = open('user_ranks_dict', 'r')
user_ranks_dict = pickle.load(fh)
fh.close()

def scores(user, L=10):
	n = len(user_totest_dict[user])
	user_ranks = user_ranks_dict[user]
	m = 0.0
	p = 0.0
	for rank_pair in user_ranks:
		if user_ranks[rank_pair][0] <= L: m = m + 1
		if user_ranks[rank_pair][1] <= L: p = p + 1
	return n, m/n, p/n

general_scores = {}
for user in user_ranks_dict:
	general_scores[user] = scores(user, L=50)
	
project_numbers = []
#popularity_score = []
#model_score = []

for user in general_scores:
	project_numbers.append(general_scores[user][0])
	#popularity_score.append(general_scores[user][2])
	#model_score.append(general_scores[user][1])

project_numbers_avg = list(set(project_numbers))
popularity_score_avg = []
model_score_avg = []

for number in project_numbers_avg:
	number_model = []
	number_popularity = []
	for user in general_scores:
		if general_scores[user][0] == number:
			number_model.append(general_scores[user][1])
			number_popularity.append(general_scores[user][2])
	model_score_avg.append(np.mean(number_model))	
	popularity_score_avg.append(np.mean(number_popularity))	

	
plt.scatter(project_numbers_avg, model_score_avg)
plt.scatter(project_numbers_avg, popularity_score_avg, color='red')
plt.xlabel('Number of projects done')
plt.title('Chance that recommendation was in top 50 per user averaged over number of projects done')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
