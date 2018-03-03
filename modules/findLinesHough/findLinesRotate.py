def findStaffLines(pages, showImage = False):
	"""
	pages = image name
	showImage will display rotated images with the lines found in red
	The output is the radians of the lines found. Horizontal lines are pi/2 

	This uses houghlines to find the staff lines. 
	A completely horizontal line would return a value of 1.5708 radians (90 degrees). 
	Lines inclined greater than 100 degrees or less than 80 degrees are ignored. 
	Lines shorter than 1/3 the width of the page are ignored. 
	"""
	img = cv2.imread(pages,1)

	#resize image. For whatever reason, 
	#if the image is really big, houghlines doesn't work as well
	###############################################################
	maxlength = 1000
	if img.shape[0] > maxlength or img.shape[1] > maxlength:
		maxL = max(img.shape[0], img.shape[1])
		scale = maxL/maxlength
		img= cv2.resize(img, (int(img.shape[0]/scale), int(img.shape[1]//scale)))


	###############################################################



	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 100, 150, apertureSize = 3)

	#the number of horizontal pixels. So if the line is greater than around those pixels.
	#Houghlines will find any straight line (horizontal or vertical). 
	#The pixel width/2.5 will give it a minimum line length. 
	horizontalPixels = img.shape[1]
	horizontalPixels = int(horizontalPixels//2.5)

	#the last argument in houghlines is the minimum threshold. 
	lines = cv2.HoughLines(edges,1,np.pi/180,horizontalPixels)

	sumTheta = 0
	count = 0

	#find average of theta
	for line in lines:
		theta = line[0][1]

		#ignore lines greater than 100 or less than 80 degrees
		#the angle is measured from the positive y axis going clockwise
		#horizontal lines are 90 degrees, but this is all in radians.  
		if theta < 1.74533 and theta > 1.39626:
			sumTheta = sumTheta + theta
			count = count + 1

	avg = sumTheta/count
	
	#to show where the lines are drawn in red. 
	if showImage:
		for line in lines:
			rho = line[0][0]
			theta = line[0][1]
			if theta < 1.74533 and theta > 1.39626:

				#code below gotten from cv2 tutorial
				a = np.cos(theta)
				b = np.sin(theta)
				x0 = a*rho
				y0 = b*rho

				x1 = int(x0 + 1000 * -b)
				y1 = int(y0 + 1000 * a)
				x2 = int(x0 - 1000 * -b)
				y2 = int(y0 - 1000 *a)

				cv2.line(img, (x1,y1),(x2,y2),(0,0,255),2)
		cv2.imshow('Lines Found', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()


	return avg


def rotateImage(pages, radians, showImage = False):
	"""
	Input
	img: image
	radians: the output of findStaffLines. It's the angle in radians. Horizontal lines are
	around pi/2

	output: rotated image
	"""
	img = cv2.imread(pages, 1)

	height = img.shape[0]
	width = img.shape[1]
	center = (width/2, height/2)

	degrees = radians*180 / np.pi #convert rad to deg
	angleCorrect = degrees - 90 #angle it needs to rotate top left by 

	rotated = cv2.getRotationMatrix2D(center, angleCorrect,1)
	rotated = cv2.warpAffine(img, rotated, (width, height))
	if showImage:
		cv2.imshow('Rotated Image', rotated)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	return rotated
