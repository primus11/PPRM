#!/usr/bin/env python
import numpy
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
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
    #pylab.figure(1)
    #pylab.clf()
    #plot = pylab.imshow(bw)
    #plot.set_cmap('gray')
    #pylab.figure(2)
    #pylab.clf()
    #plot = pylab.imshow(cb)
    #plot.set_cmap('gray')
    #pylab.figure(3)
    #pylab.clf()
    #plot = pylab.imshow(cr)
    #plot.set_cmap('gray')
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

    # We want to use 7bits for two channels (Cb, Cr), for a total of 128 different colors (= 128 clusters).
    # Default was to use 8bits for each channel (16 bits together)
    cb = numpy.reshape(cb, (width*height, 1))
    cr = numpy.reshape(cr, (width*height, 1))
    cbcr = numpy.hstack((cb, cr))
    import pdb; pdb.set_trace()
    cbcr_sample = shuffle(cbcr, random_state=0)[:1000]
    kmeans = KMeans(k=128, random_state=0).fit(cbcr_sample)
    closest = kmeans.predict(cbcr)
    codebook = kmeans.cluster_centers_

    # Convert from YCbCr back to RGB to compare
    compressed_img = numpy.zeros((height, width, 3))
    index = 0
    for i in range(height):
        for j in range(width):
            ybr = numpy.array(codebook[closest[index]], dtype=numpy.float)
            rgb = numpy.zeros((3, 1), dtype=numpy.float)
            rgb[0] = (ybr[0]-16)*255.0/219 + (ybr[2]-128)*255*0.701/112
            rgb[1] = (ybr[0]-16)*255.0/219 - (ybr[1]-128)*255*0.886*0.114/(112*0.587) - (ybr[2]-128)*255*0.701*0.299/(0.587*112)
            rgb[2] = (ybr[0]-16)*255.0/219 + (ybr[1]-128)*255*0.886/112
            compressed_img[i, j, :] = rgb
            index += 1
    pylab.figure(5)
    pylab.clf()
    pylab.imshow(compressed_img)

    pylab.show()
