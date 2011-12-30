#!/usr/bin/env python
# encoding: utf-8
import sys
from utils import data_to_na, parse_tab
from sklearn.cluster import DBSCAN
from sklearn.metrics import adjusted_rand_score, homogeneity_completeness_v_measure
import pylab

if len(sys.argv) < 4:
    sys.exit('Usage: python DBSCAN-comparison.py dataset eps min_samples')

## Data preprocessing
data = parse_tab(sys.argv[1])
eps = float(sys.argv[2])
min_samples = int(sys.argv[3])
classes = [example[-1] for example in data]
examples = data_to_na(data)

## Clustering
db = DBSCAN().fit(examples, eps=eps, min_samples=min_samples)
labels = db.labels_

## Performance evaluation
ari = adjusted_rand_score(labels, classes)
homogeneity, completeness, v_measure = homogeneity_completeness_v_measure(labels, classes)
print('ARI: {0}'.format(ari))
print('Homogeneity: {0}'.format(homogeneity))
print('Completeness: {0}'.format(completeness))
print('V-measure: {0}'.format(v_measure))

pylab.figure(1)
pylab.scatter(examples.T[0], examples.T[1], c=labels)
pylab.show()
