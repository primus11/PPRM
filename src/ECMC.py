import drawing as draw
draw.savedImages = {}

import numpy as np
import pylab as pl
from math import sqrt

execfile("data.py")
#call reloadData() if needed

class Cluster:
	def __init__(self, sample):
		self.centre = sample
		self.radius = 0
		self.members = [sample]
	def addMember(self, sample, extDist = -1):
		self.members.append(sample)
		
		if extDist != -1:
			#update cluster centre and radius
			self.radius = extDist / 2.0
			f = 1 - (extDist / 2.0) / (sqrt( sum( [(self.centre[i] - sample[i])**2 for i in range(len(sample))] )) )
			self.centre = [self.centre[i] + (f * (sample[i] - self.centre[i])) for i in range(len(sample))]
			#print(extDist / 2.0, self.centre)

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
				#search for closest centre
				for cn in clusters:
					dist = sqrt( sum( [(sample[i] - cn.centre[i])**2 for i in range(len(sample))] ) / len(sample) )
					if minDist == -1 or dist < minDist:
						minDist = dist
						minClust = cn
				

				del c.members[m]
				minClust.members.append(sample)
				
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

def ECMCThrToClusters(data, clusters):
	dataMin = min( [a[0] for a in data] )
	dataMax = max( [a[0] for a in data] )
	hr = int(100 * (dataMax - dataMin) / (clusters * 2)) #dont ask :D
	
	dif = -1
	for i in range(hr, 2*hr):#900, 1101):
		nc = getECMC(data, (i+1) / 100.0) #finding the right cluster number
		if dif == -1 or abs(len(nc) - clusters) < dif:
			dif = abs(len(nc) - clusters)
			best = nc
			
	return nc

def ECMC(data, clusters, dataNr = 0):
	clusters = ECMCThrToClusters(data, clusters)
	
	x = np.linspace(min([x[0] for x in data]), max([x[0] for x in data]))
	y = np.linspace(min([y[1] for y in data]), max([y[1] for y in data]))
	
	colors = 'bgrcmyk'
	sign = 'o*.x+'
	
	for c in range(len(clusters)):
		#circ = pl.Circle((clusters[c].centre[0], clusters[c].centre[1]), radius = clusters[c].radius, facecolor = "none")
		#ax = pl.gca()
		#ax.add_patch(circ)
		for m in clusters[c].members:
			pl.plot(m[0], m[1], sign[c/len(colors)], markerfacecolor = colors[c%len(colors)], markersize = 3)
		
	draw.setImgTitle('ECMC_test' + str(dataNr))
	draw.showImage()

test(0, ECMC)