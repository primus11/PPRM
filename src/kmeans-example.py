#!/usr/bin/env python
# encoding: utf-8
import numpy
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances
from sklearn.utils import shuffle
from scipy.misc import imread
import pylab

# Reference:
# http://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html#example-cluster-plot-color-quantization-py

# Photo from (creative commons)
# http://www.flickr.com/photos/savannahgrandfather/3376760296/

def rgb_to_ycbcr(img):
    """YCbCr conversion. Pixel values should be 0-255."""
    height, width = img.shape
    ycbcr = numpy.zeros((height, width, 3), dtype=numpy.float)
    ycbcr[:,:,0] = 16 +  img[:,:,0]*(65.481) +  img[:,:,1]*(128.553) + img[:,:,2]*(24.966)
    ycbcr[:,:,1] = 128 + img[:,:,0]*(-37.797) + img[:,:,1]*(-74.203) + img[:,:,2]*(112.0)
    ycbcr[:,:,2] = 128 + img[:,:,0]*(112.0) +   img[:,:,1]*(-93.786) + img[:,:,2]*(-18.214)
    return ycbcr

if __name__ == '__main__':
    num_colors = 64

    img = imread('../presentation/china-wall.jpg')
    img = numpy.array(img, dtype=numpy.float32) / 255
    width, height, d = img.shape
    img_array = numpy.reshape(img, (width * height, d))
    sample = shuffle(img_array, random_state=0)[:1000]
    kmeans = KMeans(k=num_colors, random_state=0)
    kmeans.fit(sample)
    codebook = kmeans.cluster_centers_
    labels = kmeans.predict(img_array)
    compressed_array = numpy.array([codebook[labels[index]] for index in range(width*height)])
    compressed = numpy.reshape(compressed_array, (width, height, d))

    codebook_random = shuffle(img_array, random_state=0)[:num_colors+1]
    distances = euclidean_distances(codebook_random, img_array, squared=True)
    labels_random = distances.argmin(axis=0)
    compressed_array_random = numpy.array([codebook_random[labels_random[index]] for index in range(width*height)])
    compressed_random = numpy.reshape(compressed_array_random, (width, height, d))

    pylab.figure(1)
    pylab.clf()
    pylab.imshow(img)

    pylab.figure(2)
    pylab.clf()
    pylab.imshow(compressed)

    pylab.figure(3)
    pylab.clf()
    pylab.imshow(compressed_random)

    pylab.show()

    import sys
    sys.exit(0)
    #barn_full_img = imread('../presentation/YCbCr-separation.jpg')
    #height = barn_full_img.shape[0] / 4
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
