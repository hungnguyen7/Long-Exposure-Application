# Hỗ trợ viết CLI(Command Line Interface)
# https://codelungtung.wordpress.com/2017/11/25/command-line-parsing-with-argparse/
import argparse
from features import contrast, changeContrast
import cv2
import math
# Create CLI interface
ap=argparse.ArgumentParser(description='Create long exposure')
ap.add_argument('-v', '--video', required=True, help='path to input video file')
ap.add_argument('-o', '--output', required=True, help='path to output image')
args=vars(ap.parse_args())

# Khởi tạo trung bình của 3 màu cơ bản
(rAvg, gAvg, bAvg)=(None, None, None)
totalFrameOfVideo=0
print('[INFO] Opening video file...')
# Mở video
stream=cv2.VideoCapture(args['video'])
print('[INFO] Computing frame averages (this will take awhile)...')
print('Frame height: '+str(stream.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('Frame width: '+str(stream.get(cv2.CAP_PROP_FRAME_WIDTH)))
print('FPS: ' + str(int(stream.get(cv2.CAP_PROP_FPS))))

frameRate = 100
# stream.set(cv2.CAP_PROP_POS_MSEC, 2000)
#Tính số frame hình trong video
while True:
    (grabbed, frame)=stream.read()
    # stream.read() returns a bool (True/False). If frame is read correctly, it will be True.
    if not grabbed:
        break
    # Lấy frame hiện tại
    frameId = stream.get(1)
    # Chia frame thành các thành phần màu cơ bản RGB
    frame_contrast = changeContrast(frame)
    (B, G, R)=cv2.split(frame_contrast.astype('float'))
    # Khởi tạo nếu (rAvg, gAvg, bAvg)=None
    if frameId % math.floor(frameRate) == 0:
        if rAvg is None:
            rAvg=R
            bAvg=B
            gAvg=G
        else:
            rAvg = ((totalFrameOfVideo * rAvg) + (1.0 * R)) / (totalFrameOfVideo + 1.0)
            gAvg = ((totalFrameOfVideo * gAvg) + (1.0 * G)) / (totalFrameOfVideo + 1.0)
            bAvg = ((totalFrameOfVideo * bAvg) + (1.0 * B)) / (totalFrameOfVideo + 1.0)
        totalFrameOfVideo+=1.0

print('Total frame: '+str(totalFrameOfVideo))



# Hợp nhất các giá trị trung bình RGB với nhau
avg=cv2.merge([bAvg, gAvg, rAvg]).astype('uint8')
cv2.imwrite(args['output'], avg)
stream.release()
print('[INFO] Success!!!')