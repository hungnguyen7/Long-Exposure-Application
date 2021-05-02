
import cv2
import math
from features import changeContrastHSV, changeRGBValue
def longExposure(videoLink, frameRate = 1, hisEqual = False, rgb = []):
    name = videoLink.split('/')[2].split('.')[0]
    # Khởi tạo trung bình của 3 màu cơ bản
    (rAvg, gAvg, bAvg)=(None, None, None)
    totalFrameOfVideo=0
    # Mở video
    stream=cv2.VideoCapture(videoLink)
    while True:
        (grabbed, frame)=stream.read()
        if not grabbed:
            break
        frameId = stream.get(1)
        if hisEqual:
            frame = changeContrastHSV(frame)
        frame = changeRGBValue(frame, rgb)
        # Chia frame thành các thành phần màu cơ bản RGB
        (B, G, R)=cv2.split(frame.astype('float'))
        # Khởi tạo nếu (rAvg, gAvg, bAvg)=None
        if frameId % math.floor(frameRate) == 0:
            if rAvg is None:
                rAvg=R
                bAvg=B
                gAvg=G
            else:
                rAvg = ((totalFrameOfVideo * rAvg) + (1 * R)) / (totalFrameOfVideo + 1)
                gAvg = ((totalFrameOfVideo * gAvg) + (1 * G)) / (totalFrameOfVideo + 1)
                bAvg = ((totalFrameOfVideo * bAvg) + (1 * B)) / (totalFrameOfVideo + 1)
            totalFrameOfVideo+=1
    # Hợp nhất các giá trị trung bình RGB với nhau
    avg=cv2.merge([bAvg, gAvg, rAvg]).astype('uint8')
    cv2.imwrite('./imgOutput/{}#{}fr.png'.format(name, frameRate), avg)
    stream.release()
    return './imgOutput/{}#{}fr.png'.format(name, frameRate)