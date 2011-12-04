import drawing as draw
draw.savedImages = {}

import numpy as np
import pylab as pl
from sklearn import cluster
from itertools import cycle
from scipy.spatial import distance

execfile("data.py")
#call reloadData() if needed


def DBSCAN(data, clusters, dataNr = 0):
	D = distance.squareform(distance.pdist(data))
	S = 1 - (D / np.max(D))

	db = cluster.DBSCAN().fit(S, eps=0.95, min_samples=10)
	core_samples = db.core_sample_indices_
	labels = db.labels_
	
	x = np.linspace(min([x[0] for x in data]), max([x[0] for x in data]))
	y = np.linspace(min([y[1] for y in data]), max([y[1] for y in data]))
	
	colors = cycle('bgrcmy')
	for k, col in zip(set(labels), colors):
		if k == -1:
			col = 'k'
			markersize = 6
		class_members = [index[0] for index in np.argwhere(labels == k)]
		cluster_core_samples = [index for index in core_samples
				if labels[index] == k]
		for index in class_members:
			x = data[index]
			if index in core_samples and k != -1:
				markersize = 14
			else:
				markersize = 6
			pl.plot(x[0], x[1], 'o', markerfacecolor = col,
					markeredgecolor = 'k', markersize = markersize)

	draw.setImgTitle('DBSCAN_test' + str(dataNr))
	draw.showImage()


test(0, DBSCAN)