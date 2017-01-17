#!/usr/bin/python3
import numpy as np
import cv2, sys, re
import urllib.request

imageLink = sys.argv[1]

def grayScale(image): 
	colors = 0
	neutron = image
	row = neutron.shape[0]
	#print(row)
	#row
	col = neutron.shape[1]
	#print(col)
	print("converting to gray")
	for r in range(row): 
		for c in range(col): 
			colors = image[r, c]
			#print (colors)
			#newColors =  +  + 
			gre = .11*colors[0] +  .59*colors[1] + .3*colors[2]
			neutron[r,c] = [gre, gre, gre]
	print("displayed")
	return neutron


def averageValue(image): 
	colors = 0 
	newImage = image 
	redTotal = 0 
	greenTotal = 0 
	blueTotal = 0
	row = newImage.shape[0]
	col = newImage.shape[1]
	totalPixels = row * col
	for r in range(row): 
		for c in range(col): 
			colors = image[r, c]
			redTotal += colors[0] 
			greenTotal += colors[1] 
			blueTotal += colors[2]
	redAvg = redTotal / totalPixels
	blueAvg = blueTotal / totalPixels
	greenAvg = greenTotal / totalPixels


def blurred(image): 
	print ("blurred")
	blur = cv2.GaussianBlur(image,(5,5),0)
	return blur


# Default image file

imgSpec = "http://ramsau.com/blog/" + \
          "wp-content/uploads/Klettersteig_Skywalk.jpg"
if len(sys.argv) > 1: imgSpec = sys.argv[1]

# Decide between file & url with regular expression (re)
if re.compile("^\\w*\\:\\/\\/").search(imgSpec) is None:
  img = cv2.imread(imgSpec, cv2.IMREAD_COLOR)
else:
  resp = urllib.request.urlopen(imgSpec)
  img = np.asarray(bytearray(resp.read()), dtype = "uint8")
  img = cv2.imdecode(img, cv2.IMREAD_COLOR)
  grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# Allows window to be resized by user (in theory)
cv2.namedWindow('imgWnd', cv2.WINDOW_NORMAL)
height, width = img.shape[:2]    # Get image dimensions
widthMax = 1024                  # The screen width, in pixels
if (width > widthMax):
  cv2.resizeWindow('imgWnd', widthMax, int(height*widthMax/width))

cv2.imshow('imgWnd',img)
origImg = img.copy()
curImg = img.copy()
isGray = False
# Now show the image
while(1):
	k = cv2.waitKey(0)
	if (k == ord('r')):
		cv2.imshow('image',origImg)
		curImg = origImg.copy()
		isGray = False
		print ("revert")
	elif (k == ord('g')):
		curImg = grayImg
		isGray = True
		cv2.imshow('image', grayImg)
	elif (k == ord('b')):
		if not isGray:
			curImg = grayImg
		blur = blurred(curImg)
		curImg = blur
		isGray = True
		cv2.imshow('image', blur)
		print ("displayed blurred")
	elif (k == 27): 
		cv2.destroyAllWindows()
		break

