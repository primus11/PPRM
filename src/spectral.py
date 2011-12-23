#!/usr/bin/env python
# encoding: utf-8
import sys
from utils import data_to_na, parse_tab
import numpy
from sklearn.cluster import SpectralClustering
from sklearn.metrics.pairwise import euclidean_distances
import pylab

if len(sys.argv) == 1:
    sys.exit('Usage: python spectral-example.py dataset')

examples = data_to_na(parse_tab(sys.argv[1]))
distances = euclidean_distances(examples, examples)
# Apply gaussian kernel as suggested in the documentation:
gamma = 0.5 # == 1 / num_features (heuristic)
similarity_matrix = numpy.exp(-distances**2 * gamma)
sc = SpectralClustering(k=3, random_state=0)
sc.fit(similarity_matrix)

labels = [label*1. for label in sc.labels_]
pylab.figure(1)
pylab.scatter(examples.T[0], examples.T[1], c=labels)
pylab.show()
