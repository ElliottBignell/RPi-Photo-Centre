import numpy as np
import cv2
from PIL import Image

# cv2.SetCaptureProperty(capture, cv.CV_CAP_PROP_BRIGHTNESS,1 )

camera = cv2.VideoCapture( 0 ) # video capture source camera (Here webcam of laptop) 

def checkCamera():

    ret,frame = camera.read() # return a single frame in variable `frame`

    cv2.imshow("image", frame)
    cv2.imwrite( './c1.jpg',frame )
    np_image = Image.open( './c1.jpg' )

    return np_image

    cv2.destroyAllWindows()

def closeCamera():
    camera.release()

