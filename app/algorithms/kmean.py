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
	maxlen = max([len(row) for row in rows])
	'''
	This for loop just filling some not null value in rows.
	For example maybe one or two or more person not sign one day, filling it with value 0.001.
	So we will get a MxM matrix.
	'''
	for i in range(len(rows)):
		if len(rows[i]) != maxlen:
			for j in range(maxlen-1):
				rows[i].append(0.001)
	'''
	Maybe a MxM matrix like this.
	[[0, 1, 2, 3],
	 [1, 2, 3, 4],
	 [3, 4, 3, 4]
	]
	We will get range like this.
	[[0, 3],
	 [1, 4],
	 [2, 3],
	 [3, 4]
	]
	Obviously, we get value range for every row.
	Then, we can generate some random list for cluster.
	For example, we can get this arrsy depend on value range.
	[2.001, 3.021, 2.246, 3.145]
	'''
	ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
		for i in range(len(rows[0]))]
	clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
		for i in range(len(rows[i]))] for j in range(k)]
	'''
	If we get same lastmatches for last loop and current loop, it's time to stop.
	'''
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