import drawing as draw
draw.savedImages = {}

from utils import data_to_na, parse_tab
import numpy as np
import sys
import pylab
import os

clusterIdx = {}
labels = []

data = parse_tab(sys.argv[1])
examples = data_to_na(data)

for d in data:
	if d[2] not in clusterIdx:
		clusterIdx[d[2]] = len(clusterIdx)
	
	labels.append(clusterIdx[d[2]])

draw.scatter(examples, labels)
draw.setImgTitle(os.path.splitext(os.path.basename(sys.argv[1]))[0])
draw.showImage()