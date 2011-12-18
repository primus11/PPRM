import numpy as np
from sklearn.datasets.samples_generator import make_blobs

dataList = []

def generateSimpleData():
	#this should generate 5 clusters
	#4 in all corners and one additional in the middle
	
	n_samples = 50

	a = np.random.randn(n_samples, 2)
	b = np.random.randn(n_samples, 2) + np.array([20, 20])
	c = np.random.randn(n_samples, 2) + np.array([0, 20])
	d = np.random.randn(n_samples, 2) + np.array([20, 0])
	e = np.random.randn(n_samples, 2) + np.array([10, 10])
	data = np.r_[a, b, c, d, e]
	
	return data, 5 #5 here is number of clusters
	
def generateBlobs():
	#not realy a big difference to a previous one...
	centers = [[1,1], [-1, 1], [1, -1]]
	data, garbage = make_blobs(n_samples=750, centers=centers, cluster_std=0.4)
	return data, len(centers)
	
def makeTestData():
	dataList.append(generateSimpleData())
	dataList.append(generateBlobs())
	
def getTestData(nr): #+format		
	return dataList[nr-1]
	
def reloadData():
	dataList = []
	
def test(dataNr, func):
	if len(dataList) == 0:
		makeTestData()
		
	if dataNr > 0:
		data, clusters = getTestData(dataNr)
		func(data, clusters, dataNr)
	else:
		for i in range(len(dataList)):
			data, clusters = getTestData(i+1)
			func(data, clusters, i+1)