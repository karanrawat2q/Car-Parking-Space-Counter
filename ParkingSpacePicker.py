from turtle import position
import cv2
import pickle # to save all the poisitioon of parking spots and the bring it to main code
# Python3 program to illustrate store efficiently using pickle module Module translates an in-memory Python object 
# into a serialized byte stream—a string of  bytes that can be written to any file-like object.
'''
cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)


x1,y1 ------
|          |
|          |
|          |
--------x2,y2
'''
width , height = 107, 48  # (157-50) , (200-192)
try:
    with(open('D:\\Local Repo\\carImgPark\\parking', 'rb')) as f:
        positionList = pickle.load(f)
except EOFError:
    positionList = []

def mouseClick(event, x, y, flags, param):
    # event botton generated coordinates x,y when clicked on the screen
    if event == cv2.EVENT_LBUTTONDOWN:  # left button clicked to draw rectangle
        positionList.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN: # right button clicked to delete rectangle
        for i,pos in enumerate(positionList):
            x1, y1 = pos
            if x1 < x < x1 +width and y1 < y  < y1+height:
                positionList.pop(i)

    with open('D:\\Local Repo\\carImgPark\\parking', 'wb') as f:
        pickle.dump(positionList, f)    

while True:
    img = cv2.imread('D:\\Local Repo\\carImgPark\\Park.png') # It will read the image again and again as if we put it outside the loop it will read only once as the image will be static therefore we need to import it again and again 
    #cv2.rectangle(img,(50,192),(157,240),(0,255,0),2)
    for pos in positionList:
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2) 
    cv2.imshow("parking spots", img)
    cv2.setMouseCallback("parking spots", mouseClick) # mouseClick is a function that will be called when mouse is clicked
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break

