#this is not really testAll but more like a runAll

import drawing as draw#reload(drawing)
draw.savedImages = {}
draw.saveImages = 1
draw.showImages = 0

execfile("GMM.py")
execfile("DBSCAN.py")