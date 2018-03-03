## making it into pdf
#16:9 aspect ratio landscape
#middle line between, the middle staff in the same. Look at the bottom of the box 

import matplotlib
matplotlib.use('TkAgg')

import os
import sys
import glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import find_lines_original as find_lines
import csv

#combines 3 images vertically with img0 on top, img1 in the middle, and img2 at the bottom

def combine3images(img0, img1 = False, img2 = False, maxHeight = None):
	#if only 1 line on the picture (ie the last page)
	#img0 and img2 just become a tiny image with height 1. 
	channels = img0.shape[2]

	if not isinstance(img1, type(img0)):
		img1 = img0
		img0 = np.ones((0, img1.shape[1], channels), np.uint8) *255
		img2 = img0
	
	#if only two lines on the page (ie the second to last page)
	elif not isinstance(img2, type(img0)):
		img2 = np.ones((0, img1.shape[1], channels), np.uint8) *255

	if maxHeight == None:
		maxHeight = max(img0.shape[0],img1.shape[0], img2.shape[0])

	maxwidth = max(img0.shape[1],img1.shape[1],img2.shape[1])
	images = [img0, img1, img2]
	finalImages = []
	
	for img in images:
		if img.shape[1] < maxwidth:
			difference = maxwidth - img.shape[1]
			height = img.shape[0]

			#append a white image so that all image widths are the maxwidth
			blank_image = np.ones((height, difference, channels), np.uint8) *255

			#attach this white image horizontally
			img = np.concatenate((img, blank_image), axis = 1)
		finalImages.append(img)
	

	height_3 = finalImages[0].shape[0] + finalImages[1].shape[0] + finalImages[2].shape[0]
	topBR = .7
	middleBR = .4
	bottomBR = .1
	heightFactor = 5
	leftTab = .1

	# the final picture should have a height width ratio of 9:16
	#there should be 4 white horizontal strips added between the 3 lines
	img = None
	
	# if the picture needs to be 'widened'
	if height_3/maxwidth > 9/16:
		#we still want space between the three lines, so we'll set the total height to have a fudge factor
		totalHeight = int(maxHeight * heightFactor)
		totalWidth = int(totalHeight / 9 *16)
		currentWidth = finalImages[0].shape[1]
		
		firstWhite = np.ones((int(bottomBR * totalHeight), currentWidth, channels), np.uint8) *255
		secondWhite = np.ones(( int((middleBR - bottomBR)* totalHeight - finalImages[2].shape[0]), currentWidth, channels), np.uint8) *255
		thirdWhite = np.ones(( int((topBR - middleBR) *totalHeight - finalImages[1].shape[0]), currentWidth, channels), np.uint8) *255
		fourthWhite = np.ones(( int((1 - topBR) * totalHeight - finalImages[0].shape[0]), currentWidth, channels), np.uint8) *255

		img = np.concatenate((fourthWhite,finalImages[0], thirdWhite, finalImages[1], secondWhite,finalImages[2], firstWhite), axis = 0)

		height = img.shape[0]
		neededWidth = abs(totalWidth - currentWidth) #should be positive anyway
		if neededWidth < totalWidth *leftTab:
			leftWhite = np.ones((height, neededWidth, channels), np.uint8) *255
			img = np.concatenate((leftWhite, img), axis = 1)

		else:
			leftWidth = int(leftTab * totalWidth)
			leftWhite = np.ones((height, leftWidth, channels), np.uint8) *255

			rightWidth = abs(neededWidth - leftWidth)
			rightWhite = np.ones((height, rightWidth, channels), np.uint8) * 255
			
			img = np.concatenate((leftWhite, img, rightWhite), axis = 1)

	#if the image neededs to be taller to fit 9:16 ratio
	else:
		currentWidth = finalImages[0].shape[1]
		totalWidth = int(currentWidth/(1-leftTab)*1) #to include a left tab
		totalHeight = int(totalWidth/16*9)

		fiW = max(int(bottomBR * totalHeight),0)
		sW = max( int((middleBR - bottomBR)* totalHeight - finalImages[2].shape[0]), 0)
		tW =  max(int((topBR - middleBR) *totalHeight - finalImages[1].shape[0]),0)
		foW = max(int((1 - topBR) * totalHeight - finalImages[0].shape[0]),0)

		firstWhite = np.ones((fiW, currentWidth, channels), np.uint8) *255
		secondWhite = np.ones(( sW, currentWidth, channels), np.uint8)*255
		thirdWhite = np.ones(( tW, currentWidth, channels), np.uint8)*255
		fourthWhite = np.ones(( foW, currentWidth, channels), np.uint8)*255


		img = np.concatenate((fourthWhite,finalImages[0], thirdWhite, finalImages[1], secondWhite,finalImages[2], firstWhite), axis = 0)
		height = img.shape[0]

		#add the white left tab
		leftWhite = np.ones((height, int(leftTab * currentWidth), channels), np.uint8)*255
		img = np.concatenate((leftWhite, img), axis = 1)

	return img

#Images must have the same number of channels (1 for BW or 3 for Color)
def attach_images_horizontally(img0, img1):
	height0 = img0.shape[0]
	height1 = img1.shape[0]
	difference = abs(height0 - height1)
	channels = img0.shape[2]

	#img0 is smaller. To concantenate images horizontally, their heights must be the same
	#this adds a white image to make the heights the same
	if height0 < height1:
		width = img0.shape[1]
		blank_image = np.ones((difference, width, channels), np.uint8) *255
		img0 = np.concatenate((blank_image, img0), axis = 0)
	else:
		width = img1.shape[1]
		blank_image = np.ones((difference, width, channels), np.uint8) *255
		img1 = np.concatenate((blank_image, img1), axis = 0)

	img = np.concatenate((img0, img1), axis = 1)
	return img



###goes through all the boxes, and concantenate ones that are too small to make 1 line
def make_lines(images):
	total = len(images)
	modifiedImages = list()

	top_line = images[0]
	middle_line = images[1]
	bottom_line = images[2]
	i = 2

	while (i < total):
		if top_line.shape[1] + middle_line.shape[1] <= bottom_line.shape[1]:
			top_line = attach_images_horizontally(top_line, middle_line)
			middle_line = bottom_line
			i = i + 1
			bottom_line = images[i]
		elif middle_line.shape[1] + bottom_line.shape[1] <= top_line.shape[1]:
			middle_line = attach_images_horizontally(middle_line, bottom_line)
			i = i + 1
			bottom_line = images[i]
		else:
			break
	modifiedImages.append(top_line)
	modifiedImages.append(middle_line)
	modifiedImages.append(bottom_line)

	i = i + 1
	while (i < total):
		top_line = middle_line
		middle_line = bottom_line
		bottom_line = images[i]


		i = i + 1
		while (i < total):
			if bottom_line.shape[1] + images[i].shape[1] <= max(top_line.shape[1], middle_line.shape[1]):
				bottom_line = attach_images_horizontally(bottom_line, images[i])
				i = i + 1
			else:
				break
		modifiedImages.append(bottom_line)
	return modifiedImages



def compile_flow(flowfile, imageDirectory, imageName):
	# extract name of directory
	dirname = os.path.dirname(flowfile)

	# boxes file
	# boxesfile = flowfile.replace("flow.csv", "boxes.csv")
	boxesfile = flowfile

	# read the flow in a list
	flow = []
	with open(flowfile) as f:
		csvr = csv.reader(f)
		next(csvr, None) # skip header
		for r in csvr:
		    flow.append(r)
	# for i in flow:
	# 	print(i)
	# read boxes and make them into a dictonary of dictionaries
	boxes = {}
	maxHeight = 0
	maxWidth = 0
	with open(boxesfile) as f:
		csvr = csv.reader(f)
		next(csvr, None) # skip header
		for r in csvr:
		    boxes[r[0]] = {"page": int(r[5]),
		                   "line": int(r[6]),
		                   "x": int(r[1]),
		                   "y": int(r[2]),
		                   "w": int(r[3]),
		                   "h": int(r[4])
		                    }
		    maxHeight = max(maxHeight, int(r[4]))
		    maxWidth = max(maxWidth, int(r[3]))

	lines = list()

	for i in range(len(boxes)):
		lines.append(boxes[str(i+1)])
	
	images = []
	count = 0
	for box in lines:
		pagefile = imageDirectory + imageName + "_" + str(box["page"]) + ".jpg"
		x = box['x']
		y = box['y']
		w = box['w']
		h = box['h']

		img = cv2.imread(pagefile)
		img = img[y:(y + h), x:(x + w), :]
		count = count + 1
		images.append(img)

	modifiedLines = make_lines(images)


	combinedImages = list()
	for i in range(len(modifiedLines) -2):
		img0 = modifiedLines[i]
		img1 = modifiedLines[i+1]
		img2 = modifiedLines[i+2]
		combinedImages.append(combine3images(img0, img1, img2, maxHeight))
	
	#this does the last two images, because there's only 2 lines on the page as opposed to 3
	if len(modifiedLines) >= 2:
		img0 = modifiedLines[-2]
		img1 = modifiedLines[-1]
		combinedImages.append(combine3images(img0, img1 = img1, maxHeight = maxHeight))

	#the last page will only have 1 line
	if len(modifiedLines) >= 1:
		img0 = modifiedLines[-1]
		combinedImages.append(combine3images(img0, maxHeight= maxHeight))


	string = ""
	for i in range(len(combinedImages)):
		string = string + imageDirectory + str(i) + ".jpg "
		cv2.imwrite(imageDirectory + str(i) + ".jpg", combinedImages[i])

	print(string)
	os.system("convert " + string + " " + imageDirectory +"pdf_out.pdf")



if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) == 1:
        # use test file
        filename = "./public/Beethoven2pages/boxes/boxes.csv"
        imageDirectory = "./public/Beethoven2pages/separatePages/"
        imageName = "Beethoven2pages"
        #image name will now be pages


        # filename = "./public/Debussy/boxes/boxes.csv"
        # imageDirectory = "./public/Debussy/separatePages/"
        # imageName = "DebussyLaMerV"
        # filename = "../test/Beethoven5_pages/flow.csv"
    else:
        filename = cl_arguments[1]
    compile_flow(filename, imageDirectory, imageName)
    print("Finished compiling!")