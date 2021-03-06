# load libraries
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def show_small_matplot(img, lab = 'this is a test', myscale = 0.7, cmap = 'gray'):
    # the images are large --- resize to show on screen
    imS = cv2.resize(img, (int(img.shape[1] * myscale), int(img.shape[0] * myscale)))   
    plt.imshow(imS, cmap=cmap)
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close()

def find_lines(patharg, 
               consider_row_black = 0.4, 
               minlineheight = 15, 
               maxlineheight = 100, 
               debug = False, 
               saveplot = True):
   ##### PARAMS
   #debug = False
   #consider_row_black = 0.70 # if xx% of more of pixels in a row are black, consider black
   #minlineheight = 15 # these values are used to filter bad lines (too narrow, too large)
   #maxlineheight = 100 

   # read original image
   original = cv2.imread(patharg)

   if debug:
      show_small_matplot(original)

   # find lines
   # 1) extract horizontal lines
   horizontal = original.copy()
   # convert to grayscale
   horizontal = cv2.cvtColor(horizontal, cv2.COLOR_BGR2GRAY)
   (thresh, horizontal) = cv2.threshold(horizontal, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   horizontal = cv2.adaptiveThreshold(cv2.bitwise_not(horizontal), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
   # prepare structure
   horizontalsize = int(horizontal.shape[1] / 20) 
   # note: if I use a value > 30, I capture also some notes; 
   # if much lower, I lose some lines
   horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, 
                               (horizontalsize,1))
   # Apply morphology operations
   horizontal = cv2.erode(horizontal, horizontalStructure, (-1, 1))
   horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, 1))

   if debug:
      show_small_matplot(horizontal)

   kernel = np.ones((6,6), np.uint8)
   horizontal = cv2.dilate(horizontal, kernel, iterations = 1)
   horizontal = cv2.bitwise_not(horizontal)

   if debug:
      show_small_matplot(horizontal)

   # find beginning and end of all lines
   nrows, ncols = horizontal.shape
   # sum the number of black pixels in each row
   black_pixels = np.sum(horizontal == 0, 1)
   black_rows = (black_pixels > consider_row_black * ncols)
   begin_end = []

   openline = 0
   closeline = nrows
   isopen = False
   for i in range(nrows):
      if black_rows[i]:
         if isopen == False:
            # open a new line
            isopen = True
            openline = i
      else:
         if isopen == True:
            # close a line
            isopen = False
            closeline = i
            if ((closeline - openline) > minlineheight) and ((closeline - openline) < maxlineheight):
               begin_end.append([openline, closeline])
   # now refine beginning and end
   begin_end_refined = begin_end.copy()
   tmp = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
   rowsums = np.sum(tmp,1)
   for i in range(len(begin_end) + 1):
      # white space above
      if i == 0:
         mystart = 0
      else:
         mystart = begin_end[i - 1][1]
      if i == (len(begin_end)):
         myend = nrows
      else:
         myend = begin_end[i][0]
      myrs = rowsums[mystart:myend] / (255 * original.shape[1])
      success = False
      cutoff = 0.995
      while not success:
         totemptylines = np.sum((myrs > cutoff) == True)
         if totemptylines > 0:
            above = np.min(np.where((myrs > cutoff) == True))
            below = np.max(np.where((myrs > cutoff) == True))
            success = True
            if i < len(begin_end):
               begin_end_refined[i][0] = begin_end[i][0] - (myrs.shape[0] - below)
            if i > 0:
               begin_end_refined[i-1][1] = begin_end[i-1][1] + above
            if debug:
               z = tmp[mystart:myend,]
               cv2.line(z, (0, above), (ncols, above), (0,0,255), 2)
               cv2.line(z, (0, below), (ncols, below), (0,0,255), 2)
               show_small_matplot(z, cmap = "Spectral")
         else:
            cutoff = cutoff - 0.005
   if saveplot:
      # draw the lines on the original
      withlines = original.copy()
      withlines = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR) 

      for z in begin_end_refined:
         cv2.line(withlines, (0, z[0]), (ncols, z[0]), (255,0,255), 2)
         cv2.line(withlines, (0, z[1]), (ncols, z[1]), (0,255,255), 2)

      show_small_matplot(withlines, cmap = "Spectral")
      #cv2.imwrite(os.path.split(patharg)[1], withlines)
   return begin_end_refined

## Run test
import glob
all_tests = glob.glob("/home/sallesina/Desktop/final/temp/*.png")

for test in all_tests:
   find_lines(test)
