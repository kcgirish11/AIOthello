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


def sobel(image, colorImage, threshold): 
	img = image.copy().astype(np.float32)
	colorImg = colorImage.copy()
	gxMat = [np.asarray([-1, 0, 1]), np.asarray([-2, 0, 2]), np.asarray([-1, 0, 1])]
	gyMat = [np.asarray([-1, -2, -1]), np.asarray([0, 0, 0]), np.asarray([1, 2, 1])]
	matX = np.asarray(gxMat)
	matY = np.asarray(gyMat)
	xImg = cv2.filter2D(img, -1, matX)
	yImg = cv2.filter2D(img, -1, matY)
	row = img.shape[0]
	col = img.shape[1]
	for r in range(row): 
		for c in range(col): 
			xCol = xImg[r][c]
			gx = xCol
			#print ("gx", gx)
			yCol = yImg[r][c]
			gy = yCol
			#print ("gy", gy)
			squared = (gx * gx) + (gy * gy)
			#print ("Squared", squared)
			if (squared > threshold):
				colorImg[r][c] = [255,0,0]
	return colorImg.astype(np.uint8)


def calcAngle(x, y): 
	t = atan2(x,y)
	if 0 <= t <= pi/4:
		return 0
	if pi/4<= t <= pi/2:
		return 1
	if pi/2 <= t <=3*pi/4:
		return 2
	if 3*pi/4<= t<= pi:
		return 3
	if pi<= t <= 5*pi/4:
		return 0
	if 5*pi/4 <= t <=3*pi/2:
		return 1
	if 3*pi/2 <= t <= 7*pi/4:
		return 2
	return 3

def canny(image, grayImg): 
	# image is already sobel
	img = image.copy().astype(np.float32)
	colorImg = colorImage.copy()
	gxMat = [np.asarray([-1, 0, 1]), np.asarray([-2, 0, 2]), np.asarray([-1, 0, 1])]
	gyMat = [np.asarray([-1, -2, -1]), np.asarray([0, 0, 0]), np.asarray([1, 2, 1])]
	matX = np.asarray(gxMat)
	matY = np.asarray(gyMat)
	xImg = cv2.filter2D(img, -1, matX)
	yImg = cv2.filter2D(img, -1, matY)
	row = img.shape[0]
	col = img.shape[1]
	for r in range(row): 
		for c in range(col): 
			if not (r == 0 or c == 0 or r == row - 1 or c == col -1):
				xCol = xImg[r][c]
				gx = xCol
				#print ("gx", gx)
				yCol = yImg[r][c]
				gy = yCol
				#print ("gy", gy)
				mag = sqrt((gx * gx) + (gy * gy)) 
				theta = calcAngle(gx, gy) 
				if theta == 0: 
					a = img[r][c+1]
					b = img[r][c-1]
				elif theta == 1: 
					a = img[r-1][c+1]
					b = img[r+1][c-1]
				elif theta == 2: 
					a = img[r-1][c]
					b = img[r+1][c]
				elif theta == 3: 
					a = img[r-1][c-1]
					b = img[r+1][c+1]

				if(a > mag or b > mag): 
					grayImg[r][c] = 0 
				else: 
					grayImg[r][c] = 1
	return grayImg.astype(np.uint8)




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
isSobel = False
thresh = sys.argv[2]
# Now show the image

cv2.imshow('image', origImg)
cv2.waitKey(0)
blur = blurred(origImg)
sobImg = sobel(blur, origImg, int(thresh))
cv2.imshow('image', sobImg)
cv2.waitKey(0)
cannyImg = canny(sobImg, grayImg)
cv2.imshow('image', cannyImg)
cv2.waitKey(0)
cv2.destroyAllWindows()

# while(1):
# 	k = cv2.waitKey(0)
# 	if (k == ord('r')):
# 		cv2.imshow('image', origImg)
# 		curImg = origImg.copy()
# 		isGray = False
# 		print ("revert")
# 	elif (k == ord('g')):
# 		curImg = grayImg
# 		isGray = True
# 		cv2.imshow('image', grayImg)
# 	elif (k == ord('b')):
# 		if not isGray:
# 			curImg = grayImg
# 		blur = blurred(curImg)
# 		curImg = blur
# 		isGray = True
# 		cv2.imshow('image', blur)
# 		print ("displayed blurred")
# 	elif (k == ord('s')): 
# 		if not isGray: 
# 			curImg = grayImg
# 		sobImg = sobel(curImg, origImg, int(thresh))
# 		cv2.imshow('image',  sobImg)
# 		isGray = True
# 		isSobel = True
# 	elif (k == 27): 
# 		cv2.destroyAllWindows()
# 		break

