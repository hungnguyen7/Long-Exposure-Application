import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline


def changeContrastHSV(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_hsv[:, :, 2] = cv2.equalizeHist(img_hsv[:, :, 2])
    img_output = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    return img_output

def changeRGBValue(img, arrValueToChange):
    (B, G, R) = cv2.split(img.astype('float'))
    R+=arrValueToChange[0]
    G+=arrValueToChange[1]
    B+=arrValueToChange[2]
    result=cv2.merge([B, G, R]).astype('float')
    return result

def brightnessControl(image, level):
    return cv2.convertScaleAbs(image, beta=level)

def spreadLookupTable(x, y):
    spline = UnivariateSpline(x, y)
    return spline(range(256))

increaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 80, 160, 256])
decreaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 50, 100, 256])
def warmImage(image):
    blue_channel, green_channel, red_channel = cv2.split(image)
    red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
    return cv2.merge((blue_channel, green_channel, red_channel))

def coldImage(image):
    blue_channel, green_channel, red_channel = cv2.split(image)
    red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    return cv2.merge((blue_channel, green_channel, red_channel))