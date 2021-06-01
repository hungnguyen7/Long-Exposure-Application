
import cv2
import math
from features import changeContrastHSV, changeRGBValue
def longExposure(videoLink, name, frameRate):
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
        frame = changeContrastHSV(frame)
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
    cv2.imwrite('{}#{}fr.png'.format(name, frameRate), avg)
    print('Done video: {}'.format(videoLink))
    stream.release()
videos = ['IMG_8588']
for rate in range(1, 2):
    for i in range(len(videos)):
        longExposure('data/03/' + videos[i] + '.MOV', 'output/contrast/'+ videos[i], rate*1)
    print('Done rate:  ' + str(rate*1))