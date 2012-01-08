#!/usr/bin/env python
# encoding: utf-8
from utils import data_to_na, parse_tab
from sklearn.metrics import adjusted_rand_score, homogeneity_completeness_v_measure
import pylab

#data = parse_tab('../datasets/circle-weird.tab')
#output = '../datasets/nested-circle-output'
#data = parse_tab('../datasets/half-moons.tab')
#output = '../datasets/half-moons-output'
data = parse_tab('../datasets/red-blue-clusters.tab')
output = '../datasets/red-blue-output'


classes = [example[-1] for example in data]
examples = data_to_na(data)
labels = map(int, open(output).read().split())
print len(labels), len(classes)

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
