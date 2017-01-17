import numpy as np
import cv2, sys, re, math
import urllib.request
from fractions import Fraction

def getSlope(gy, gx):
    temp = math.atan2(gy,gx)
    #print(gy, gx)
    return math.tan(temp)
    #return gy/gx

def drawline(Circle, Gx, Gy, row, col, edges):
    if Gx[row, col] ==0:
        slope = 0
    else:
        slope = getSlope(Gy[row, col], Gx[row, col])
    edges[(row, col)] = (slope, ((-1*slope*col)+row))
    #num = slope.numerator
    #denom = slope.denominator
    #print(str(denom))
    xchange = 0
    ychange = 0

    while row+ychange>0 and row+ychange<Circle.shape[0] and col+xchange >0 and col+xchange<Circle.shape[1]:
        Circle[int(row+ychange), int(col+xchange)][0]+=1
        xchange+=1
        ychange+=slope
    xchange = 0
    ychange = 0
    while row-ychange>0 and row-ychange<Circle.shape[0] and col-xchange >0 and col-xchange<Circle.shape[1]:
        Circle[int(row-ychange), int(col-xchange)][0]+=1
        xchange+=1
        ychange+=slope
    #print("B")

def findCenter(image, Gx, Gy):
    Circle = np.zeros_like(image)
    Edges = {}
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            if image[row,col][1] == 0:
                drawline(Circle, Gx , Gy, row, col, Edges)
    return (((1.0*Circle)/np.max(Circle)*255).astype(np.uint8), Edges)

def intersections(center, Edges, Centers):
    crow, ccol  = center
    #print(Edges)
    for edge in Edges:
        slope, intercept= Edges[edge]
        erow, ecol = edge
        #print(crow==erow)
        if int(slope*ccol)+int(intercept) in range(crow-1, crow+1):
            #print(str(erow-crow))
            #print(str(ecol-ccol))
            #print()
            Centers[center].append(((erow-crow)*(erow-crow)) + ((ecol-ccol)*(ecol-ccol)))



def frequency(Centers):
    Circles = {}
    frequency = {}
    last = 0
    currd = 15
    keys = []
    for center in Centers:
        Circles[center] = set([])
        ctr = sorted(Centers[center])
        posCenters =set([(ctr[int(len(ctr)/2)])])
        for r in range(len(ctr)):
            if ctr[r] >0:
                continue
            elif r == 0:
                frequency[ctr[r]] = 1
                keys.append(r)
                #currd = float(1.0*(ctr[r+1] - ctr[r])/20)
                last = r
            else:
                if ctr[r]< ctr[last]+currd:
                    frequency[ctr[last]]+=1
                else:
                    frequency[ctr[r]] = 1
                    keys.append(r)
                    last = r
                    #if r< len(ctr):
                        #currd = float(1.0*(ctr[r+1] - ctr[r])/2)
        #posCenters = set([])
        #print(len(frequency.keys())==len(keys))
        for r in range(len(keys)):
            if len(frequency) == 1:
                posCenters.add(keys[0])
            else:
                if r==0:
                    if frequency[r]>frequency[r+1]:
                        posCenters.add(frequency[r]+200)
                elif r<len(keys):
                    if max(frequency[r], frequency[r-1], frequency[r+1]) == frequency[r]:
                        posCenters.add(frequency[r]+200)
                else:
                    if frequency[r]>frequency[r-1]:
                        posCenters.add(frequency[r]+200)
        posCenters.add(1600)
        Circles[center] = posCenters
        #print(posCenters)
    return Circles

def drawCircles(Circles, img):
    Newimg = np.copy(img)
    Huff = (np.copy(img)*0)
    for center in Circles:
        for r in Circles[center]:
            centernew = (center[1], center[0])
            #cv2.circle(Huff,centernew, int(math.sqrt(r)), [255,255,255])
            #cv2.circle(Newimg, centernew, int(math.sqrt(212)), [255,0,0])
            cv2.circle(Newimg,centernew, int(math.sqrt(r)), [255,0,0])
    return (Newimg, Huff)


def findCircles(image, Gx, Gy):
    Lineimg, Edges = findCenter(np.copy(image), Gx, Gy)
    Center = Lineimg > 150
    Center = Center> 0
    Center = 255*Center
    Centers = {}
    Poscenter = np.where(Center==255)
    print(Poscenter)
    #for i in range(len(Poscenter)):
        #print(i)
    Centers[244,573 ] = []
    Centers[488,337] = []

    for center in Centers:
        row, col = center
        intersections(center, Edges, Centers)
        #print(Centers)
        #print(Centers[center])
    Circles = frequency(Centers)
    #print(Circles)
    #drawnImage = drawCircles(Circles, image)

    return Circles



url = "https://www.krispykreme.com/SharedContent/User/aa/aa0ef72f-77be-4fef-8d43-bca50c530085.png"
#url = "Orignal.jpg"
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
Edges = cv2.cvtColor(255-cv2.Canny(img.copy(), 100, 200),cv2.COLOR_GRAY2RGB)
Circle = np.copy(Edges)
#drawline(Edges,img, 10, 10)

gx = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
gy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
#print(image)
blur = 255-(cv2.cvtColor(cv2.GaussianBlur(img.copy(),(7,7),0), cv2.COLOR_BGR2GRAY))
#print(gray)
Gx = cv2.filter2D(1.0*blur, -1, gx)
Gy = cv2.filter2D(1.0*blur, -1, gy)
#image = Gx*Gx +Gy*Gy
cv2.imshow("Canny2", Edges)
cv2.imshow("original", img)
Transpose, Huff = drawCircles(findCircles(Edges,Gx, Gy), img)
cv2.imshow("Edge", Huff)
cv2.imshow("Transpose", Transpose)
cv2.waitKey(0)
cv2.destroyAllWindows()
