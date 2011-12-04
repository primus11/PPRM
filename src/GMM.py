import drawing as draw
draw.savedImages = {}

import numpy as np
import pylab as pl
from sklearn import mixture

execfile("data.py")
#call reloadData() if needed


def GMM(data, clusters, dataNr = 0):
	clf = mixture.GMM(n_components=clusters) #, cvtype='full')
	clf.fit(data)
	
	x = np.linspace(min([x[0] for x in data]), max([x[0] for x in data]))
	y = np.linspace(min([y[1] for y in data]), max([y[1] for y in data]))
	X, Y = np.meshgrid(x, y)
	XX = np.c_[X.ravel(), Y.ravel()]

	Z = np.log(-clf.eval(XX)[0])
	Z = Z.reshape(X.shape)

	pl.contour(X, Y, Z)

	pl.scatter(data[:, 0], data[:, 1], .8)

	draw.setImgTitle('GMM_test' + str(dataNr))
	draw.showImage()


test(0, GMM)