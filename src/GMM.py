execfile("drawing.py")

import numpy as np
import pylab as pl
from sklearn import mixture

execfile("data.py")

def GMM(data, clusters):
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

	setImgTitle('GMM')
	showImage()


def testGMM(testNr):
	global showImages
	showImages = 1
	if testNr > 0:
		GMM(getTestData(testNr))
	else:
		for i in range(allTests):
			data, clusters = getTestData(i)
			GMM(data, clusters)
	showImages = 0
			
#testGMM(0)