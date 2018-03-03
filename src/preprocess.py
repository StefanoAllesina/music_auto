import os
import sys
import glob
import cv2
import numpy as np
from matplotlib import pyplot as plt
import find_lines
import csv
    
### SHOWING IMAGES
def press(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key=='x':
        visible = xl.get_visible()
        xl.set_visible(not visible)
        fig.canvas.draw()

def show_image(img, lab = 'this is a test', myscale = 0.6, cmap = 'gray'):
    """
    show an image, rescaled so that it fits the screen
    pressing the x button closes the image
    """
    imS = cv2.resize(img, (int(img.shape[1] * myscale), int(img.shape[0] * myscale))) 
    fig, ax = plt.subplots() 
    fig.canvas.mpl_connect('key_press_event', press)
    im = ax.imshow(imS, cmap=cmap)
    plt.show()

### ACTUAL CODE
def extract_pages(filename):
    # extract relevant info from filename
    pdfname = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    musicname = pdfname.split(".pdf")[0]
    dirpages = dirname + "/"+ musicname + "_pages/"
    dirdebug = dirname + "/"+ musicname + "_debug/" # to store files for debug
    # create directory
    if not os.path.isdir(dirpages):
        tmp = os.system("mkdir " + dirpages)
    if not os.path.isdir(dirdebug):
        tmp = os.system("mkdir " + dirdebug)
    # burst pdf
    tmp = os.system("pdftk " + filename + " burst")
    # move pages to rigth location
    tmp = os.system("mv pg_* " + dirpages)
    return (musicname, dirpages, dirdebug)

def rotate_page(patharg):
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
    # show the output image
    # print("rotating" + patharg + " [INFO] angle: {:.3f}".format(angle), end = "\r")
    # overwrite image
    cv2.imwrite(patharg, rotated)
    return 0

def convert_page(ff):
    #print("converting to jpg file " + ff + "...", end = "\r")
    os.system("convert -density 300 " + ff + " " + ff[:-4] + ".jpg")
    # remove the pdf as we don't need it anymore
    os.system("rm " + ff)
    return 0

def clean_page(page):
    img = cv2.imread(page,0)
    ret,thresh1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY) # Note: 100 as threshold is quite generous
    # clean image by erosion + dilation
    # this is supposed to be a very gentle cleaning --- maybe too gentle?
    kernel1 = np.ones((3,3), np.uint8)
    kernel2 = np.ones((2,2), np.uint8)
    img_erosion = cv2.erode(thresh1, kernel1, iterations=1)
    img_dilation = cv2.dilate(img_erosion, kernel2, iterations=1)
    # overwrite previous image
    cv2.imwrite(page, img_dilation)
    return 0


def preprocess(filename):
    # Step 1: burst pdf 
    musicname, dirpages, dirdebug = extract_pages(filename)
    # Step 2: for each page, convert to jpg, do some cleaning, rotate, and attempt finding lines
    pages = glob.glob(dirpages + "/*.pdf")
    npages = len(pages)
    # open files for writing output boxes and flow
    out_boxes = open(dirpages + "/boxes.csv", "w")
    boxes_writer = csv.writer(out_boxes)
    boxes_writer.writerow(["box_id", "line", "page", "x", "y", "w", "h"])
    out_flow = open(dirpages + "/flow.csv", "w")
    flow_writer = csv.writer(out_flow)
    flow_writer.writerow(["desc", "box_id"])
    for i in range(1, npages + 1):
        # this is to keep analyzing pages in order... not so pretty
        page = dirpages + "pg_" + ("0000" + str(i))[-4:] + ".pdf"
        print("processing page ", page)
        convert_page(page)
        page_jpg = page[:-4] + ".jpg"
        print("processing image ", page_jpg)
        clean_page(page_jpg)
        rotate_page(page_jpg)
        boxes = find_lines.find_boxes(page_jpg, debug = "save")
        if len(boxes) > 0:
            flow_writer.writerow(["# Start Page " + str(boxes[0]["p"]), "NA"])
        for b in boxes:
            bid = str(b["p"]) + "_" +  str(b["l"])
            boxes_writer.writerow([bid, b["l"], b["p"], b["x"], b["y"], b["w"], b["h"]])
            flow_writer.writerow([b["message"], bid])
    out_boxes.close()
    out_flow.close()
        

if __name__ == '__main__':
    cl_arguments = sys.argv
    if len(cl_arguments) == 1:
        # use test file
        filename = "../test/Beethoven5.pdf"
    else:
        filename = cl_arguments[1]
    preprocess(filename)
    print("Finished preprocessing!")

