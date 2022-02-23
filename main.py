# we need to crop images inside the rectangle and the we need to find a way if there is a car inside a rectangle
# Wheather this region has car present on it we can do it by lokking at pixel count 
#We will convert the image in binaray image based on its edges and corners and from there we can say that if the image doesn't have lots of edges and corners then it plane image else it is a car image
# To do that 
import cv2
import numpy as np
import pickle
import cvzone

cap = cv2.VideoCapture('D:\\Local Repo\\carImgPark\\carPark.mp4')

with open('D:\\Local Repo\\carImgPark\\parking', 'rb') as f:
    positionList = pickle.load(f)

width , height = 107, 48  # (157-50) , (200-192)

def checkParkingSpace(imgDialate):

    spaceCounter = 0

    for pos in positionList: 
        x,y = pos
        # crop the image and the 
        imgCrop = imgDilate[y:y+height, x:x+width]
        # cv2.imshow('img'+str(x*y), imgCrop)

        # Counting the no of white pixels in the image
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(frame, str(count), (x,y+height-5), scale=1,thickness=2,offset=1)

        if count < 1900:
            color = (0,255,0)
            thickness = 5
            spaceCounter +=1
        else:
            color = (0,0,255)
            thickness = 2
        
        # To display all the rectangle on the video
        cv2.rectangle(frame, (x,y), (x+width,y+height), color, thickness)
    
    cvzone.putTextRect(frame,f' Free: {spaceCounter}/{len(positionList)}',(100,50), scale=3,thickness=5,offset=20,colorR=(0,200,0))

    
while True:
    # To Loop the Video : We are resetting the frame everytime if it reaches total amount of frames that video has
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == cap.get(cv2.CAP_PROP_POS_FRAMES):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0) 
    
    _, frame = cap.read()
    # Thresholding the image
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)


    """edge detection on an image that has already had Gaussian Blur 
    applied to it to reduce noise, as well as use an upper and lower threshold to help."""
    sigma = np.std(imgBlur)
    mean = np.mean(imgBlur)
    lower = int(max(0, (mean - sigma)))
    upper = int(min(255, (mean + sigma)))

    # Converthing the image to binary image using Canny edge detection #! It seems to me better method than  adaptive thresholding
    imgCanny = cv2.Canny(imgBlur, lower, upper) # The value of lower and upper are determined by trial and error one work is (50,150)

    # # Median Blur to remove noise #! Not seems to work with canny edge detection 

    # Dilation filter will thicken the edges where as erosion will thin the edges
    imgDilate = cv2.dilate(imgCanny, np.ones((3,3), np.uint8), iterations=2) # more iterations will thicken the edges

    checkParkingSpace(imgDilate)

    frame = cv2.resize(frame, (1280, 720))

    cv2.imshow('frame', frame)
    #cv2.imshow('imgDilate', imgDilate)
    
    # to slow down the video by a factor of 10
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break 