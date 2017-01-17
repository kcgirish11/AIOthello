
#!/usr/bin/python3
import numpy as np, math
import cv2, sys, re
import urllib.request

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


def canny(image):
  return cv2.Canny(image.copy(), 100, 200)

def hough(image):
  #print ("here")
  canny_img = canny(image)
  img = canny_img
  Gx = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
  Gy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
  blur = 255-(cv2.cvtColor(cv2.GaussianBlur(image.copy(),(7,7),0), cv2.COLOR_BGR2GRAY))
  xImg = cv2.filter2D(1.0*blur, -1, Gx)
  yImg = cv2.filter2D(1.0*blur, -1, Gy)
  edges = {}
  row = img.shape[0]
  col = img.shape[1]
  Circle = np.zeros_like(img)
  #print ("threshold canny", threshold)
  for r in range(row):
    for c in range(col):
      if not (r == 0 or c == 0 or r == row - 1 or c == col -1):
        gx = xImg[r][c]
        gy = yImg[r][c]
        if canny_img[r][c] == 255:
          temp = math.atan2(gy, gx)
          perp_slope = math.tan(temp)
          edges[(r, c)] = (perp_slope, ((-1*perp_slope*c)+r))
          deltaX = 0
          deltaY = 0
          while r+deltaY > 0 and r+deltaY<Circle.shape[0] and c+deltaX>0 and c+deltaX<Circle.shape[1]:
              Circle[int(r+deltaY)] [int(c+deltaX)] += 1
              deltaX += 1
              deltaY += perp_slope
          deltaX = 0
          deltaY = 0
          while r-deltaY > 0 and r-deltaY<Circle.shape[0] and c-deltaX>0 and c-deltaX<Circle.shape[1]:
              Circle[int(r-deltaY)][int(c-deltaX)]+= 1
              deltaX += 1
              deltaY += perp_slope

  return ((((1.0*Circle)/np.max(Circle)*255).astype(np.uint8)), edges)

def Compare(r,uniq):
    error = 3
    if len(uniq)==0:
        return r
    for rad in uniq:
        if int(r) in range(   int(    rad   -   (rad*error/100)) ,int(    rad   +  (rad*error/100)    )   ):
            return rad
    return r
def findCenters(center_img, edges, img):
    new_img = np.copy(center_img)
    row = center_img.shape[0]
    col = center_img.shape[1]
    diag = np.sqrt(row*row +col*col)
    new_img = new_img > 150
    new_img = new_img * 255
    circle_img = np.copy(img)
    nonUnique = set()
    realCenters = set()
    centers = {}
    trueCenter = {}
    cimg = np.copy(img)
    for r in range(row):
        for c in range (col):
            if new_img[r][c] == 255:
                centers[(r,c)] = []
                #cv2.circle(cimg,(c,r),2,(0,0,0),2)
    #cv2.imshow("pre-distance center",cimg)
    #print(len(centers))
    for center in centers:
        if center not in nonUnique:
            #print(center)
        #realCenters[center] = []
            for center2 in centers:
              if center2 not in nonUnique and center != center2:
                #print(center2)
                (r1, c1) = center
                (r2, c2) = center2
                distance = np.sqrt((r1-r2)*(r1-r2) + (c1-c2)*(c1-c2))
                if distance < 3.5:
                  nonUnique.add(center2)
                else:
                  #print(1)
                  realCenters.add(center2)
    #print(len(realCenters))
    realCenters = realCenters-nonUnique
    #print(len(realCenters))
    for center in realCenters:
        trueCenter[center] = []
        #cv2.circle(cimg,center,10,(0,0,0))
    centers = trueCenter
  
    print ("edges", len(edges))
    #print(len(centers))
    for center in centers:
        for edge in edges:
          (r, c) = edge
          #print (edge)
          (x, y) = center
          #print (center)
          (slope, yInter) = edges[edge]
          if (int(slope*x + yInter)) in range(y-3,y+3):
            #print ('here')
            centers[center].append( np.sqrt(    (   (r-x)*(r-x) ) + (   (c-y)*(c-y) )   )    )
            #print (np.sqrt(    (   (r-y)*(r-y) ) + (   (c-x)*(c-x) )   ) )
          ncenter = (y, x) 
          cv2.circle(cimg,ncenter,10,(0,0,0))
            #circle_img[r][c] = 0
    #print(centers)
    cv2.imshow("center",cimg)
    cv2.waitKey(0)


    frequencyRadius = {}
    circles = set()
    for center in centers:
        #print ("CENTER", center)
        radius = centers[center]
        print (radius)
        for r in radius:
          #print(r)
          #error = 5
          #print("radius", r)
          #new_radius = range(   int(    r   -   (r*error/100) ),int(    r   +  (r*error/100)    )   )
          radii = Compare(r,frequencyRadius)
          if radii not in frequencyRadius:
            frequencyRadius[int(radii)] = 1
          else:
            frequencyRadius[int(radii)] += 1

    #print(frequencyRadius)
        for r in frequencyRadius:
          #print ("here", r)
          #print ("frequencyRadius" , frequencyRadius[r])
          if (frequencyRadius[r]/r) > 1/2:
            #print ("actual value" + str(r) )
            circles.add(    (   center,r   )     )
            (x, y) = center
            #print (center)
            new_center = (y, x)
            cv2.circle(circle_img, new_center, int(r), 0)
            print ("center", center)
            print("radius", r)
    for key in sorted(frequencyRadius.keys()): 
      print (key, (frequencyRadius[key]/r))
    return circle_img

def houghFake(img):
  cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
  circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=0,maxRadius=0)
  circles = np.uint16(np.around(circles))
  for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
  return cimg


url = imageLink
if len(sys.argv)>1:
    url = sys.argv[1]
if re.compile("^\\w*\\:\\/\\/").search(url) is None:
  img = cv2.imread(url, cv2.IMREAD_COLOR)

else:
  resp = urllib.request.urlopen(url)
  img = np.asarray(bytearray(resp.read()), dtype = "uint8")
  img = cv2.imdecode(img, cv2.IMREAD_COLOR)

(Circle, edges) = hough(img)
#print (edges)
# cannyimg = canny(img)
# cv2.imshow('image', cannyimg)
#print (edges)
Circles = findCenters(Circle,edges,img)
cv2.imshow('image', Circle)
cv2.waitKey(0)
cv2.imshow('circle',Circles)
img = cv2.medianBlur(img,5)
#cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
#circle_img = houghFake(img)
#cv2.imshow('circle_image', circle_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
