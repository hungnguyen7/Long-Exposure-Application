import cv2
import numpy as np
from matplotlib import pyplot as plt

from os import listdir
from os.path import isfile, join

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

# onlyfiles = [f for f in listdir('./output/test') if isfile(join('./output/test', f))]
# for i in onlyfiles:
#     for r in range(1, 10):
#         for g in range(1, 10):
#             for b in range(1, 10):
#                     image = cv2.imread('./output/test/{filename}'.format(filename=i))
#                     re=changeRGBValue(image, [r*10, g*10, -b*10])
#                     cv2.imwrite('./output/increseYellow/{r}-{g}-{b}--{file}'.format(r=r*10, g=g*10, b=-b*10, file=i), re)
# filename = 'IMG_8588#1fr.png'
# image = cv2.imread('./output/test/{file}'.format(file=filename))
# image=changeContrastHSV(image)

# for r in range(1, 10):
#     for g in range(1, 10):
#         for b in range(1, 10):
#                 re=changeRGBValue(image, [r*10, g*10, -b*10])
#                 cv2.imwrite('./output/increseYellow/{r}-{g}-{b}-hope.png'.format(r=r*10, g=g*10, b=-b*10), re)