#!/usr/bin/env python
import numpy
from sklearn.cluster import KMeans
from scipy.misc import imread
import pylab

if __name__ == '__main__':
    barn_full_img = imread('../presentation/YCbCr-separation.jpg')
    height = barn_full_img.shape[0] / 4
    img = barn_full_img[:height,:,:]
    width = img.shape[1]
    bw = numpy.zeros((height, width), dtype=numpy.float)
    cb = numpy.zeros((height, width), dtype=numpy.float)
    cr = numpy.zeros((height, width), dtype=numpy.float)
    # YCbCr conversion
    bw[:,:] = 16 + img[:,:,0]*65.481 + img[:,:,1]*128.553 + img[:,:,2]*24.966
    cb[:,:] = 128 + img[:,:,0]*(-37.797) + img[:,:,1]*(-74.203) + img[:,:,2]*112.0
    cr[:,:] = 128 + img[:,:,0]*112.0 + img[:,:,1]*(-93.786) + img[:,:,2]*(-18.214)
    # Display all three channels
    # TODO: use appropriate colors instead of gray levels only
    pylab.figure(1)
    pylab.clf()
    plot = pylab.imshow(bw)
    plot.set_cmap('gray')
    pylab.figure(2)
    pylab.clf()
    plot = pylab.imshow(cb)
    plot.set_cmap('gray')
    pylab.figure(3)
    pylab.clf()
    plot = pylab.imshow(cr)
    plot.set_cmap('gray')
    # Count color combinations (Cb, Cr)
    bw = numpy.array(bw, dtype=numpy.uint8)
    cb = numpy.array(cb, dtype=numpy.uint8)
    cr = numpy.array(cr, dtype=numpy.uint8)
    histogram = numpy.zeros((256, 256), dtype=numpy.int)
    for i in range(height):
        for j in range(width):
            histogram[cb[i, j], cr[i, j]] += 1
    # Most used colors (clusters are not very distinct in this example):
    # TODO: maybe do another example like
    # http://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html#example-cluster-plot-color-quantization-py
    pylab.figure(4)
    pylab.clf()
    plot = pylab.imshow(histogram>10000)
    plot.set_cmap('gray')

    # We want to use 7bits for two channels (Cb, Cr), for a total of 128 different colors (= 128 clusters)
    cbcr = numpy.vstack((cb, cr)).T
    cbcr_sample = numpy.shuffle(cbcr, random_state=0)[:1000]
    kmeans = KMeans(k=128, random_state=0).fit(cbcr_sample)
    labels = kmeans.predict(cbcr)

    pylab.show()
