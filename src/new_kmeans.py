#!/usr/bin/env python
# encoding: utf-8
import sys
from utils import data_to_na, parse_tab, addToResult
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, homogeneity_completeness_v_measure
import pylab
import os
import drawing as draw
draw.savedImages = {}

if len(sys.argv) < 3:
    sys.exit('Usage: python kmeans.py dataset k')

## Data preprocessing
data = parse_tab(sys.argv[1])
k = int(sys.argv[2])
classes = [example[-1] for example in data]
examples = data_to_na(data)

## Clustering
kmeans = KMeans(k=k, random_state=0)
kmeans.fit(examples)
codebook = kmeans.cluster_centers_
labels = kmeans.predict(examples)

## Performance evaluation
ari = adjusted_rand_score(labels, classes)
homogeneity, completeness, v_measure = homogeneity_completeness_v_measure(labels, classes)
print('ARI: {0}'.format(ari))
print('Homogeneity: {0}'.format(homogeneity))
print('Completeness: {0}'.format(completeness))
print('V-measure: {0}'.format(v_measure))
addToResult('k-means', ari, homogeneity, completeness, v_measure)

draw.scatter(examples, labels)
print(os.path.splitext(os.path.basename(sys.argv[1]))[0])
draw.setImgTitle('kmeans_' + os.path.splitext(os.path.basename(sys.argv[1]))[0])
draw.showImage()