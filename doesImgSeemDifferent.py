import cv2
import numpy
def doesImgSeemDifferent(p1, p2):
    threshhold = 125
    diff = cv2.absdiff(p1,p2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ret, img_thresh = cv2.threshold(gray, 32, 255, cv2.THRESH_BINARY)
    count = numpy.sum(img_thresh == 255)
    return ( 30 < count )
