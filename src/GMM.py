import drawing as draw
draw.savedImages = {}

import numpy as np
import pylab as pl
from sklearn import mixture

execfile("data.py")


def GMM(data, clusters, dataNr = 0):
	clf = mixture.GMM(n_components=5) #, cvtype='full')
	clf.fit(data)

	x = np.linspace(-10.0, 30.0)
	y = np.linspace(-10.0, 30.0)
	X, Y = np.meshgrid(x, y)
	XX = np.c_[X.ravel(), Y.ravel()]

	Z = np.log(-clf.eval(XX)[0])
	Z = Z.reshape(X.shape)

	pl.contour(X, Y, Z)

	pl.scatter(data[:, 0], data[:, 1], .8)

	draw.setImgTitle('GMM_test' + str(dataNr))
	draw.showImage()


def testGMM(dataNr):
	draw.showImages = 1
	if dataNr > 0:
		data, clusters = getTestData(dataNr)
		GMM(data, clusters, dataNr)
	else:
		for i in range(testCount):
			data, clusters = getTestData(i+1)
			GMM(data, clusters, dataNr+1)
	draw.showImages = 0

	
testGMM(0)