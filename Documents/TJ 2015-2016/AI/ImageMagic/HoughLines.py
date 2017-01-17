import numpy as np
import cv2, sys, re, math
import urllib.request
from fractions import Fraction

imageLink = sys.argv[1]
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

def hough_transform(img):
  
  row = img.shape[0]
  col = img.shape[1]
  diagnol = np.sqrt((row*row) + (col*col))
  plot = np.zeros((181,int(2*diagnol+1))
  for ang in range(181):
    d = row*math.cos(ang) + col*math.sin(ang)
    index = ang/d +181

  for rowIdx in range(nR):
    for colIdx in range(nC):
      if img_bin[rowIdx, colIdx]:
        for thIdx in range(len(theta)):
          rhoVal = colIdx*np.cos(theta[thIdx]*np.pi/180.0) + \
              rowIdx*np.sin(theta[thIdx]*np.pi/180)
          rhoIdx = np.nonzero(np.abs(rho-rhoVal) == np.min(np.abs(rho-rhoVal)))[0]
          H[rhoIdx[0], thIdx] += 1
  return rho, theta, H


url = imageLink
if len(sys.argv)>1:
    url = sys.argv[1]
if re.compile("^\\w*\\:\\/\\/").search(url) is None:
  img = cv2.imread(url, cv2.IMREAD_COLOR)

else:
  resp = urllib.request.urlopen(url)
  img = np.asarray(bytearray(resp.read()), dtype = "uint8")
  img = cv2.imdecode(img, cv2.IMREAD_COLOR)

# Allows window to be resized by user (in theory)
cv2.namedWindow('imgWnd', cv2.WINDOW_NORMAL)
height, width = img.shape[:2]    # Get image dimensions
widthMax = 1024                  # The screen width, in pixels

if (width > widthMax):
  cv2.resizeWindow('imgWnd', widthMax, int(height*widthMax/width))
#cv2.imshow("Edge", img)
#drawline(Edges,img, 10, 10)


gx = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
gy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
# #print(image)
blur = 255-(cv2.cvtColor(cv2.GaussianBlur(img.copy(),(7,7),0), cv2.COLOR_BGR2GRAY))
# #print(gray)
theta_res = 1
rho_res = 1
rho, theta, H = hough_transform(blur, theta_res, rho_res)
# cv2.waitKey(0)
# cv2.imshow("hough lines", H)
cv2.waitKey(0)
cv2.destroyAllWindows()
