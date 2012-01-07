showImages = 0
saveImages = 1
imgFilename = 'default'
savedImages = {}
imageTitle = ''

import pylab

def setImgTitle(title):
	global imgFilename #...
	global savedImages
	
	pylab.title(title)
	imageTitle = title
	
	title.replace
	title = title.replace(' ', '')[:25] #taking only first x characters...
	if not savedImages.has_key(title):
		imgFilename = title
		savedImages[title] = 0
	else:
		savedImages[title] += 1
		imgFilename = title + str(savedImages[title]) #setting name + number (so it's not overwritten)

		
def showImage():
	global imgFilename #...
	global saveImages
	global showImages
	
	if saveImages == 1:
		pylab.savefig("images/" + imgFilename+ ".png")
		pylab.title("")
		pylab.savefig("images/" + imgFilename+ ".pdf")

	if showImages == 1:
		pylab.title(imageTitle)
		pylab.show() #if need for title remember it and "draw" it again
	else:
		pylab.clf()
		imgFilename = "default"
		
def scatter(examples, labels):
	markers = 'osD+*xh'
	colors = 'rgbcmky'
	
	idx = {}
	
	for i in range(len(labels)):
		if labels[i] not in idx:
			idx[labels[i]] = len(idx)
			
		pylab.scatter(examples[i].T[1], examples[i].T[0], c=colors[idx[labels[i]]], marker=markers[idx[labels[i]]])
	