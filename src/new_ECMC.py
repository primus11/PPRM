import drawing as draw
draw.savedImages = {}

import numpy as np
import pylab
from math import sqrt
import os
import sys
from sklearn import mixture
from sklearn.metrics import adjusted_rand_score, homogeneity_completeness_v_measure
from utils import data_to_na, parse_tab, addToResult

class Cluster:
	memberIdx = 0
	def __init__(self, sample):
		self.centre = sample
		self.radius = 0
		self.members = [sample]
		self.membersIdx = [Cluster.memberIdx]
		Cluster.memberIdx = Cluster.memberIdx + 1
	def addMember(self, sample, extDist = -1):
		self.members.append(sample)
		self.membersIdx.append(Cluster.memberIdx)
		Cluster.memberIdx = Cluster.memberIdx + 1
		
		if extDist != -1:
			#update cluster centre and radius
			self.radius = extDist / 2.0
			f = 1 - (extDist / 2.0) / (sqrt( sum( [(self.centre[i] - sample[i])**2 for i in range(len(sample))] )) )
			self.centre = [self.centre[i] + (f * (sample[i] - self.centre[i])) for i in range(len(sample))]
			#print(extDist / 2.0, self.centre)

def getLabels(clusters, data):
	labels = []
	for i in range(len(data)):
		found = False
		
		#find in which cluster next data is
		for c in range(len(clusters)):
			for idx in clusters[c].membersIdx:
				if idx == i:
					labels.append(c) #cluster nr
					Found = True
					break
					
			if found:
				break
				
	return labels
			
def getEucDist(x1, x2):
	return sqrt( sum( [(x1[i] - x2[i])**2 for i in range(len(x1))] ) / len(x1) )
			
def getECM(data, Dthr):	
	clusters = []
	
	for sample in data:
		minDist = -1
		#minCluster
		minExtDist = -1
		#minExtCluster
		for c in clusters:
			dist = sqrt( sum( [(sample[i] - c.centre[i])**2 for i in range(len(sample))] ) / len(sample) ) #calculating normalized euclidean distance
			
			if (minDist == -1 or dist<minDist) and c.radius > dist:
				minDist = dist
				minCluster = c
			if minExtDist == -1 or dist + c.radius < minExtDist:
				minExtDist = dist + c.radius
				minExtCluster = c

		if minDist != -1:
			minCluster.addMember( sample )
			continue

		#if len(clusters) > 0:
		#	print(sample, minExtDist, 2*Dthr, clusters[0].centre, clusters[0].radius)
		if minExtDist != -1 and minExtDist <= 2 * Dthr:
			minExtCluster.addMember( sample, minExtDist)
			continue
			
		clusters.append( Cluster(sample) )
		
	return clusters
		
def getECMC(data, Dthr):
	clusters = getECM(data, Dthr)
	oldJ = -1
	
	for i in range(100):
		for c in clusters:
			for m in range(len(c.members)-1,0,-1):
				minDist = -1
				sample = c.members[m]
				sampleIdx = c.membersIdx[m]
				#search for closest centre
				for cn in clusters:
					dist = sqrt( sum( [(sample[i] - cn.centre[i])**2 for i in range(len(sample))] ) / len(sample) )
					if minDist == -1 or dist < minDist:
						minDist = dist
						minClust = cn
				

				del c.members[m]
				del c.membersIdx[m]
				minClust.members.append(sample)
				minClust.membersIdx.append(sampleIdx)
				
		for c in clusters:
			for i in range(len(c.centre)):
				c.centre[i] = sum( [m[i] for m in c.members] ) / len(c.members)

			#c.centre = [c.centre[i] + f * (o[i] - c.centre[i]) for i in range(len(c.centre))]
				
			c.radius = max([sqrt( sum( [(sample[i] - c.centre[i])**2 for i in range(len(sample))] ) / len(sample) )
						for sample in c.members])

		J = sum(
				[sum(
					[sqrt( sum( [(sample[i] - c.centre[i])**2 for i in range(len(sample))] ) / len(sample) )
						for sample in c.members]
				) for c in clusters]
			)
		#print(J)
		if oldJ != -1 and abs(oldJ - J) < 0.00001:
			break
		oldJ = J
	
	#print(J)
	return clusters

	
if len(sys.argv) < 3:
    sys.exit('Usage: python kmeans.py dataset dthr')
	
## Data preprocessing
data = parse_tab(sys.argv[1])
dthr = float(sys.argv[2])
classes = [example[-1] for example in data]
examples = data_to_na(data)

## Clustering
clusters = getECMC(examples, dthr)
labels = getLabels(clusters, examples)

## Performance evaluation
ari = adjusted_rand_score(labels, classes)
homogeneity, completeness, v_measure = homogeneity_completeness_v_measure(labels, classes)
print('ARI: {0}'.format(ari))
print('Homogeneity: {0}'.format(homogeneity))
print('Completeness: {0}'.format(completeness))
print('V-measure: {0}'.format(v_measure))
addToResult('ECMC', ari, homogeneity, completeness, v_measure)

draw.scatter(examples, labels)
print(os.path.splitext(os.path.basename(sys.argv[1]))[0])
draw.setImgTitle('ECMC_' + os.path.splitext(os.path.basename(sys.argv[1]))[0])
draw.showImage()