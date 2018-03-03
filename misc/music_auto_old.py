# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import argparse
import subprocess
import csv
import sys
import os

def show_small(img, lab = 'this is a test'):
    # the images are large --- resize to show on screen
    imS = cv2.resize(img, (850, 1100))   
    cv2.imshow(lab, imS)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def repeats_image():
	path = filedialog.askopenfilename()

	im = cv2.imread(path)
	imNoLines = cv2.imread(path)
	cv2.namedWindow("repeats", cv2.WINDOW_NORMAL)
	imS=cv2.resize(im,(0,0),fx=0.5,fy=0.5)
	imCut=cv2.resize(imNoLines,(0,0),fx=0.5,fy=0.5)
	im2 = cv2.imread(path)
	dimen=[]
	i=0
	while i<3:
		fromCenter = False
		showCrosshair = False
		r = cv2.selectROI("repeats", imS, fromCenter, showCrosshair)
		imCrop = im2[2*int(r[1]):2*int(r[1]+r[3]), 2*int(r[0]):2*int(r[0]+r[2])]
		saver = path.split('.png')
		imgAdd = saver[0]+"_repeats"+str(i)+".png"
		dimen.append([2*int(r[1]),2*int(r[1]+r[3]),2*int(r[0]),2*int(r[0]+r[2])])
		if r[2] != 0.0 and r[3] != 0.0:
		    cv2.imwrite(imgAdd, imCrop)
		cv2.waitKey(0)
		cv2.destroyWindow("repeats")
		i+=1
	print (dimen)
	imCrop = im2[0:dimen[2][0], 0:1000]
	saver = path.split('.png')
	imgAdd = saver[0]+"_upper.png"
	#dimen.append([r[0],r[1],r[2],r[3]])
	if r[2] != 0.0 and r[3] != 0.0:
		cv2.imwrite(imgAdd, imCrop)
	imCrop = im2[dimen[1][0]:dimen[1][0]+1000, dimen[1][2]:dimen[1][2]+1000]
	saver = path.split('.png')
	imgAdd = saver[0]+"_lower.png"
	#dimen.append([r[0],r[1],r[2],r[3]])
	if r[2] != 0.0 and r[3] != 0.0:
		cv2.imwrite(imgAdd, imCrop)
	callrepeat()
	
def callrepeat():
	print ("start")
	#if you get error with subprocess.call try 'chmod +x file.sh' in cmd
	subprocess.call([os.getcwd()+"/repeatjoin.sh"])
	print ("end")

def concat_image():
    global e
    string = e.get()
    return string


def join_image():
	if concat_image() == '':
		print ('please enter a valid number to for staff join iteration')
		exit(0)
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	j=1
	for f in files:
		if "___cropped___" in f:
			
			originalFname=f.split("___cropped___")[0][0:len(f[0])-2] + str(j)+'_final.png'
			print (originalFname)
			i=1
			concatArg=''
			while i<=int(concat_image()):
				concatArg+=(f+' ')
				i+=1
				
			#if you get error with subprocess.call try 'chmod +x file.sh' in cmd
			print ("start")
			print (os.getcwd()+"/concat.sh")
			subprocess.call([os.getcwd()+"/concat.sh",concatArg,originalFname])
			print ("end")
			j+=1


def rotate_image(patharg):
	#patharg = filedialog.askopenfilename()
	
	# load the image from disk
	image = cv2.imread(patharg)

	# convert the image to grayscale and flip the foreground
	# and background to ensure foreground is now "white" and
	# the background is "black"
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bitwise_not(gray)
	 
	# threshold the image, setting all foreground pixels to
	# 255 and all background pixels to 0
	thresh = cv2.threshold(gray, 0, 255,
	    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


	# grab the (x, y) coordinates of all pixel values that
	# are greater than zero, then use these coordinates to
	# compute a rotated bounding box that contains all
	# coordinates
	coords = np.column_stack(np.where(thresh > 0))
	angle = cv2.minAreaRect(coords)[-1]
	 
	# the `cv2.minAreaRect` function returns values in the
	# range [-90, 0); as the rectangle rotates clockwise the
	# returned angle trends to 0 -- in this special case we
	# need to add 90 degrees to the angle
	if angle < -45:
	    angle = -(90 + angle)
	 
	# otherwise, just take the inverse of the angle to make
	# it positive
	else:
	    angle = -angle


	# rotate the image to deskew it
	(h, w) = image.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(image, M, (w, h),
	    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


	# draw the correction angle on the image so we can validate it
	#cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
	    #(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	 
	# show the output image
	print(patharg + " [INFO] angle: {:.3f}".format(angle))
	#cv2.imshow("Input", image)
	#cv2.imshow("Rotated", rotated)
	#saver = path.split('.png')
	#imgAdd=saver[0]+"_rotated.png"
	#print (imgAdd)
	cv2.imwrite(patharg, rotated)
	#cv2.waitKey(0)

def select_image():
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	j=1
	for f in files:
		if ".pdf" in f:
			origF=f.split('.')[0]
			
			print ("start")
			#if you get error with subprocess.call try 'chmod +x file.sh' in cmd
			subprocess.call([os.getcwd()+"/burst_pdf.sh", f, origF])
			print ("end")
			break

	mypath = os.getcwd() + '/temp'
	files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f))]
	
	j=1
	
	for f in files:
		print (f)
		if all([".png" in f, "___cropped___" not in f, '-0000' not in f]):
			rotate_image(os.getcwd()+'/temp/'+f)
	# grab a reference to the image panels
	#global panelA
 
	# open a file chooser dialog and allow the user to select an input
	# image
	path = filedialog.askopenfilename()

	newP=path.split('.')
	indexPic=int(newP[0][len(newP[0])-1])
	print (indexPic)

	while True:
		from pathlib import Path
		myfile=Path(newP[0][0:len(newP[0])-1] + str(indexPic) + '.png')
		
		print(myfile)
		if myfile.is_file():
			
			path = newP[0][0:len(newP[0])-1] + str(indexPic) + '.png'
			indexPic+=1
			# ensure a file path was selected
			if len(path) > 0:
				# load the image from disk, convert it to grayscale, and detect
				# edges in it
				image = cv2.imread(path)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				#edged = cv2.Canny(gray, 50, 100)
		 
				# OpenCV represents images in BGR order; however PIL represents
				# images in RGB order, so we need to swap the channels
				image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		 
				# convert the images to PIL format...
				image = Image.fromarray(image)
				#edged = Image.fromarray(edged)
		 
				# ...and then to ImageTk format
				image = ImageTk.PhotoImage(image)
				#edged = ImageTk.PhotoImage(edged)
						# if the panels are None, initialize them
				fname = path
				img = cv2.imread(fname)
				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				img2 = cv2.adaptiveThreshold(cv2.bitwise_not(img), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)


				# 3) Horizontal lines
				horizontal = img2.copy()
				# prepare structure
				horizontalsize = int(horizontal.shape[1] / 20) 
				# note: if I use a value > 30, I capture also some notes; 
				# if much lower, I lose some lines
				horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, 
				                                                (horizontalsize,1))
				## Apply morphology operations
				horizontal = cv2.erode(horizontal, horizontalStructure, (-1, 1))
				horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, 1))

				show_small(horizontal)
				kernel = np.ones((5,5), np.uint8)
				horizontal = cv2.dilate(horizontal, kernel, iterations = 1)
				horizontal = cv2.bitwise_not(horizontal)
				show_small(horizontal)
				 


				# In[ ]:

				# 4) Vertical stuff
				vertical = img2.copy()
				# prepare structure
				verticalsize = int(vertical.shape[0] / 650) 
				verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, 
				                                                (1, verticalsize))
				## Apply morphology operations
				vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
				vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))
				#show_small(vertical)


				#x and y axis
				rs = np.sum(1- horizontal, axis =1)
				cl = list(range(horizontal.shape[0]))


				import matplotlib.pyplot as plt
				from matplotlib import interactive
				interactive(True)
				plt.axhline(y = 6)
				import scipy.interpolate
				f = scipy.interpolate.interp1d(cl, rs, kind = 'cubic')
				plt1 = plt.plot(cl, rs, 'o', cl, f(cl), '--')


				def savitzky_golay(y, window_size, order, deriv=0, rate=1):


				    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
				    The Savitzky-Golay filter removes high frequency noise from data.
				    It has the advantage of preserving the original shape and
				    features of the signal better than other types of filtering
				    approaches, such as moving averages techniques.
				    Parameters
				    ----------
				    y : array_like, shape (N,)
				        the values of the time history of the signal.
				    window_size : int
				        the length of the window. Must be an odd integer number.
				    order : int
				        the order of the polynomial used in the filtering.
				        Must be less then `window_size` - 1.
				    deriv: int
				        the order of the derivative to compute (default = 0 means only smoothing)
				    Returns
				    -------
				    ys : ndarray, shape (N)
				        the smoothed signal (or it's n-th derivative).
				    Notes
				    -----
				    The Savitzky-Golay is a type of low-pass filter, particularly
				    suited for smoothing noisy data. The main idea behind this
				    approach is to make for each point a least-square fit with a
				    polynomial of high order over a odd-sized window centered at
				    the point.
				    Examples
				    --------
				    t = np.linspace(-4, 4, 500)
				    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
				    ysg = savitzky_golay(y, window_size=31, order=4)
				    import matplotlib.pyplot as plt
				    plt.plot(t, y, label='Noisy signal')
				    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
				    plt.plot(t, ysg, 'r', label='Filtered signal')
				    plt.legend()
				    plt.show()
				    References
				    ----------
				    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
				       Data by Simplified Least Squares Procedures. Analytical
				       Chemistry, 1964, 36 (8), pp 1627-1639.
				    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
				       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
				       Cambridge University Press ISBN-13: 9780521880688
				    """
				    import numpy as np
				    from math import factorial
				    
				    try:
				        window_size = np.abs(np.int(window_size))
				        order = np.abs(np.int(order))
				    except ValueError:
				        raise ValueError("window_size and order have to be of type int")
				    if window_size % 2 != 1 or window_size < 1:
				        raise TypeError("window_size size must be a positive odd number")
				    if window_size < order + 2:
				        raise TypeError("window_size is too small for the polynomials order")
				    order_range = range(order+1)
				    half_window = (window_size -1) // 2
				    # precompute coefficients
				    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
				    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
				    # pad the signal at the extremes with
				    # values taken from the signal itself
				    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
				    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
				    y = np.concatenate((firstvals, y, lastvals))
				    return np.convolve( m[::-1], y, mode='valid')
				x = cl
				y = rs
				from scipy.signal import savgol_filter as sf
				yhat = sf(y, 191, 3) # window size 191, polynomial order 3
				plt2 = plt.plot(x, y, '.', x, yhat,'-')
				#plt.show(plt.plot(x, y, 'o'))

				new = np.histogram(rs, bins = 50)

				#from peakdetect import peakdetect
				#cb = np.array(yhat)
				#peaks = peakdetect(cb, lookahead=100)

				xyArray=[x,yhat]

				def FindMaxima(numbers):


				  maxima = []
				  length = len(numbers[1])
				  if length >= 2:
				    if numbers[1][0] > numbers[1][1]:
				      maxima.append([numbers[0][0], numbers[1][0]])
				    if length > 3:
				      for i in range(1, length-1):
				        if numbers[1][i] > numbers[1][i-1] and numbers[1][i] > numbers[1][i-2] and numbers[1][i] > numbers[1][i-3] and numbers[1][i] > numbers[1][i-4] and numbers[1][i] > numbers[1][i-5] and numbers[1][i] > numbers[1][i+1] and numbers[1][i] > numbers[1][i+2] and numbers[1][i] > numbers[1][i+3] and numbers[1][i] > numbers[1][i+4] and numbers[1][i] > numbers[1][i+5]:
				            maxima.append([numbers[0][i],numbers[1][i]])
				            maxima.append([numbers[0][i],numbers[1][i]])
				    if numbers[1][length-1] > numbers[1][length-2]:    
				      maxima.append([numbers[0][length-1],numbers[1][length-1]])        
				  return maxima
				   
				maximaArray = FindMaxima(xyArray)

				maxAr=[]
				import csv
				import sys

				x=0
				y=1
				freq=[]
				while y<len(maximaArray):
					freq.append(maximaArray[y][0]-maximaArray[x][0])
					x+=1
					y+=1
				count, division = np.histogram(freq)
				secLarge=sorted(count, reverse=True)[1]
				a=0
				while a<len(count):
					if secLarge == count[a]:
						threshh=division[a]
					a+=1
				print(threshh)

				fn = 'localMaxima_OUTPUT.csv'
				with open(fn, 'w') as myfile:
				    outputFile = csv.writer(myfile)
				    i=0
				    j=1
				    startStaff='false'
				    while j<len(maximaArray):
				    	if (maximaArray[j][0]-maximaArray[i][0])>(threshh):
				    		outputFile.writerow([maximaArray[i][0],maximaArray[i][1]])
				    		maxAr.append(maximaArray[i])
				    	else:
				    		maxAr.append(maximaArray[i-1])
				    	i+=1
				    	j+=1
				    myfile.close()
				print (maxAr)
				# maximaArray = FindMaxima(xyArray)
				# maxAr=[]
				
				# i=0
				# j=1

				# while j<len(maximaArray):
				# 	if maximaArray[j][1]>((maximaArray[int(len(maximaArray)/2)][1]/3)*2):
				# 		maxAr.append(maximaArray[j])
				# 	i+=1
				# 	j+=1


				import ctypes
				if __name__ == '__main__' :
					# Read image
					im = cv2.imread(path)
					imNoLines = cv2.imread(path)
					i=1
					j=2
					#c=0
					rectangles=[]
					
					colors=[(255,147,0), (21,152,34), (255,147,170), (244,250,34), (102,102,153),(153,0,255),
					(255,153,0)]
					c=1
					while j<len(maxAr):
					    # if i==0:
					    #     y=maxAr[i][0]-50
					    # else:
					    y = maxAr[i][0]
					    
					    h = maxAr[j][0]
					    
					    x = 50+h-y
					    import random
					    crop_rect = cv2.rectangle(im,(0,y),(1000,h),random.choice(colors),2)
					    rectangles.append(crop_rect)
					    crop_img = img[y:h, 0:1000]
					    saver = path.split('.png')
					    imgAdd = saver[0]+"___cropped___"+str(y)+".png"

					    cv2.imwrite(imgAdd,crop_img)
					    i+=2
					    j+=2
					    c+=2


					cv2.namedWindow("output", cv2.WINDOW_NORMAL)
					imS=cv2.resize(im,(0,0),fx=0.5,fy=0.5)
					imCut=cv2.resize(imNoLines,(0,0),fx=0.5,fy=0.5)
					im2 = cv2.imread(path)

					while True:


						fromCenter = False
						showCrosshair = False
						r = cv2.selectROI("output", imS, fromCenter, showCrosshair)
						imCrop = im2[2*int(r[1]):2*int(r[1]+r[3]), 0:1000]
				
						# if the 'r' key is pressed, reset the cropping region
						# if key == ord("i"):
						# 	image = clone.copy()
						# 	imCrop = clone[2*int(r[1])+25:2*int(r[1]+r[3]), 0:1000]
						# 	cv2.imshow(imCrop)
						# 	cv2.waitKey(0)
					 
						# # if the 'c' key is pressed, break from the loop
						# elif key == ord("m"):
						# 	image = clone.copy()
						# 	imCrop = clone[2*int(r[1])-25:2*int(r[1]+r[3]), 0:1000]
						# 	cv2.imshow(imCrop)
						# 	cv2.waitKey(0)
						# Crop image
						#imCrop = im2[2*int(r[1]):2*int(r[1]+r[3]), 2*int(r[0]):2*int(r[0]+r[2])]
						

						saver = path.split('.png')
						
						#imgReturn=saver[0]+"_croppedimage*.png"

						if r[2] != 0.0 and r[3] != 0.0:
							yC=2*int(r[1])
							hC=2*int(r[1]+r[3])
							print (yC)
							yFix= (min(maxAr, key=lambda x,:abs(yC-x[0]))[0])
							print (hC)
							hFix= (min(maxAr, key=lambda x,:abs(hC-x[1]))[0])

							imgAdd = saver[0]+"___cropped___"+str(yFix)+".png"

							cv2.imwrite(imgAdd, imCrop)
						else:
							break
						cv2.waitKey(0)
						cv2.destroyWindow("output")
						i+=1
		    
		else:
			cv2.waitKey(0)
			cv2.destroyWindow("output")
			break
			
		


	
# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None
e = Entry(root)
e.pack()
e.focus_set()



# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI


btn = Button(root, text="Crop an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

btn1 = Button(root, text="Edit repeats on an image", command=repeats_image)
btn1.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

btn3 = Button(root, text="Join an image", command=join_image)
btn3.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")



 
# kick off the GUI
root.mainloop()
