from math import sqrt
import random

def person(v1, v2):
	sum1 = sum(v1)
	sum2 = sum(v2)
	
	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])
	
	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])
		
	num = pSum - (sum1*sum2/len(v1))
	den = sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
	if den == 0:
		return 0
	return 1.0-num/den

def kcluster(rows, distance=person, k=10):
	ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
		for i in range(len(rows[0]))]
	clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
		for i in range(len(rows[0]))] for j in range(k)]
	
	lastmatches = None
	for t in range(100):
		bestmatches = [[] for i in range(k)]
		for j in range(len(rows)):
			row = rows[j]
			bestmatch = 0
			for i in range(k):
				d = distance(clusters[i], row)
				if d < distance(clusters[bestmatch], row):
					bestmatch = i
			bestmatches[bestmatch].append(j)
		if bestmatches == lastmatches:
			break
		lastmatches = bestmatches
		for i in range(k):
			avgs = [0.0] * len(rows[0])
			if len(bestmatches[i]) > 0:
				for rowid in bestmatches[i]:
					for m in range(len(rows[rowid])):
						avgs[m] += rows[rowid][m]
				for j in range(len(avgs)):
					avgs[j] /= len(bestmatches[i])
				clusters[i] = avgs
	return bestmatches
