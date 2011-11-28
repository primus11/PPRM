#this is not really testAll but more like a runAll

import drawing as draw#reload(drawing)
draw.savedImages = {} #i wonder if there is a way that part of module executable statemens are executed
	#also... i know that this may not be the best solution
draw.saveImages = 1

execfile("GMM.py")