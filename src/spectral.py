#!/usr/bin/env python
# encoding: utf-8
import sys
from utils import data_to_na, parse_tab
import numpy
from sklearn.cluster import SpectralClustering
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics import adjusted_rand_score, homogeneity_completeness_v_measure
import pylab

if len(sys.argv) < 3:
    sys.exit('Usage: python spectral-example.py dataset k')

## Data preprocessing
data = parse_tab(sys.argv[1])
k = int(sys.argv[2])
classes = [example[-1] for example in data]

examples = data_to_na(data)
distances = euclidean_distances(examples, examples)
# Apply gaussian kernel as suggested in the documentation:
gamma = 0.5 # == 1 / num_features (heuristic)
similarity_matrix = numpy.exp(-distances * gamma)

## Clustering
sc = SpectralClustering(k=k, random_state=0)
sc.fit(similarity_matrix)

## Performance evaluation
ari = adjusted_rand_score(sc.labels_, classes)
homogeneity, completeness, v_measure = homogeneity_completeness_v_measure(sc.labels_, classes)
print('ARI: {0}'.format(ari))
print('Homogeneity: {0}'.format(homogeneity))
print('Completeness: {0}'.format(completeness))
print('V-measure: {0}'.format(v_measure))

pylab.figure(1)
pylab.scatter(examples.T[0], examples.T[1], c=sc.labels_)
pylab.show()
