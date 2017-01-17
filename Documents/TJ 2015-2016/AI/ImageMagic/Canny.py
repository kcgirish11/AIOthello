#!/usr/bin/python3
import numpy as np
import cv2, sys, re
import urllib.request

imageLink = sys.argv[1]
pi = np.pi

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


def sobel(image, grayImg, threshold): 
	img = image.copy().astype(np.float32)
	print ("sobel threshold", threshold)
	grayImage = grayImg.copy()
	gxMat = np.asarray([np.asarray([-1, 0, 1]), np.asarray([-2, 0, 2]), np.asarray([-1, 0, 1])])
	gyMat = np.asarray([np.asarray([-1, -2, -1]), np.asarray([0, 0, 0]), np.asarray([1, 2, 1])])
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
				grayImage[r][c] = 0
			else: 
				grayImage[r][c] = 255
	return grayImage.astype(np.uint8)


def calcAngle(x, y): 
	t = np.arctan2(y, x)
	if t < 0: 
		t = 2*pi + t
	#print ("t", t)
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

def canny1(image, grayImg, threshold): 
	# image is already sobel
	img = image.copy().astype(np.float32)
	gxMat = [np.asarray([-1, 0, 1]), np.asarray([-2, 0, 2]), np.asarray([-1, 0, 1])]
	gyMat = [np.asarray([-1, -2, -1]), np.asarray([0, 0, 0]), np.asarray([1, 2, 1])]
	matX = np.asarray(gxMat)
	matY = np.asarray(gyMat)
	xImg = cv2.filter2D(img, -1, matX)
	yImg = cv2.filter2D(img, -1, matY)
	magMatrix = xImg*xImg + yImg*yImg
	row = img.shape[0]
	col = img.shape[1]
	#print ("threshold canny", threshold)
	for r in range(row): 
		for c in range(col): 
			if not (r == 0 or c == 0 or r == row - 1 or c == col -1):
				xCol = xImg[r][c]
				gx = xCol
				#print ("gx", gx)
				yCol = yImg[r][c]
				gy = yCol
				#print ("gy", gy)
				mag = magMatrix[r][c]
				#print ("color 1 ", img[r][c])
				img[r][c] = 255
				if mag < threshold: 
					continue
				theta = calcAngle(gx, gy) 
				if theta == 0: 
					a = magMatrix[r][c+1]
					b = magMatrix[r][c-1]
				elif theta == 1: 
					a = magMatrix[r-1][c+1]
					b = magMatrix[r+1][c-1]
				elif theta == 2: 
					a = magMatrix[r-1][c]
					b = magMatrix[r+1][c]
				elif theta == 3: 
					a = magMatrix[r-1][c-1]
					b = magMatrix[r+1][c+1]
				if(a > mag or b > mag): 
					img[r][c] = 255
				else: 
					img[r][c] = 0
				#print ("color 2" , img[r][c])
			else: 
				img[r][c] = 255
	return img.astype(np.uint8)

def cannyLiar(image): 
	return 255 - cv2.Canny(image, 100, 100)
def canny2(image, maxVal, minVal): 
	img = image.copy().astype(np.float32)
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
				mag = (gx * gx) + (gy * gy)
				if mag < minVal: 
					img[r][c] = 255
				if mag > maxVal: 
					theta = calcAngle(gx, gy) 
					if theta == 0: 
						a = (xImg[r][c+1] * xImg[r][c+1]) + (yImg[r][c+1] * yImg[r][c+1])
						b = (xImg[r][c-1] * xImg[r][c-1]) + (yImg[r][c-1] * yImg[r][c-1])
					elif theta == 1: 
						a = (xImg[r-1][c+1] * xImg[r-1][c+1]) + (yImg[r-1][c+1] * yImg[r-1][c+1])
						b = (xImg[r+1][c-1] * xImg[r+1][c-1]) + (yImg[r+1][c-1] * yImg[r+1][c-1])
					elif theta == 2: 
						a = (xImg[r-1][c] * xImg[r-1][c]) + (yImg[r-1][c] * yImg[r-1][c])
						b = (xImg[r+1][c] * xImg[r+1][c]) + (yImg[r+1][c] * yImg[r+1][c])
					elif theta == 3: 
						a = (xImg[r-1][c-1] * xImg[r-1][c-1]) + (yImg[r-1][c-1] * yImg[r-1][c-1])
						b = (xImg[r+1][c+1] * xImg[r+1][c+1]) + (yImg[r+1][c+1] * yImg[r+1][c+1])
					if(a > mag or b > mag): 
						img[r][c] = 255
					else: 
						img[r][c] = 0
				
	return img.astype(np.uint8)



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
minValue = int(sys.argv[2])
maxValue = int(sys.argv[3])
# Now show the image

cv2.imshow('image', origImg)
cv2.waitKey(0)
blurImg = blurred(grayImg)
sobImg = sobel(blurImg, grayImg, maxValue)
cv2.imshow('image', sobImg)
cv2.waitKey(0)
cannyImg = canny1(blurImg, grayImg, maxValue)
cv2.imshow('image', cannyImg)
print ("canny1")
cv2.waitKey(0)
canny2Img = cannyLiar(grayImg)
cv2.imshow('image', canny2Img)
print ("canny2")
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

