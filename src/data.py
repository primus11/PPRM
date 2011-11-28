import numpy

testCount = 1	

def getTestData(nr): #+format
	if nr == 1:
		return generateSimpleData()

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