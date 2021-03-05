# Hỗ trợ viết CLI(Command Line Interface)
# https://codelungtung.wordpress.com/2017/11/25/command-line-parsing-with-argparse/
import argparse
import imutils
import cv2
# Create CLI interface
ap=argparse.ArgumentParser(description='Create long exposure')
ap.add_argument('-v', '--video', required=True, help='path to input video file')
ap.add_argument('-o', '--output', required=True, help='path to output image')
args=vars(ap.parse_args())

# Initialization
# Khởi tạo trung bình của 3 màu cơ bản
(rAvg, gAvg, bAvg)=(None, None, None)
totalFrameOfVideo=0
print('[INFO] Opening video file...')
# Mở video
stream=cv2.VideoCapture(args['video'])
print('[INFO] Computing frame averages (this will take awhile)...')
#Tính số frame hình trong video
while True:
    (grabbed, frame)=stream.read()
    # stream.read() returns a bool (True/False). If frame is read correctly, it will be True.
    if not grabbed:
        break
    # Chia frame thành các thành phần màu cơ bản RGB
    (B, G, R)=cv2.split(frame.astype('float'))
    # Khởi tạo nếu (rAvg, gAvg, bAvg)=None
    if rAvg is None:
        rAvg=R
        bAvg=B
        gAvg=G
    else:
        rAvg = ((totalFrameOfVideo * rAvg) + (1 * R)) / (totalFrameOfVideo + 0.99999)
        gAvg = ((totalFrameOfVideo * gAvg) + (1 * G)) / (totalFrameOfVideo + 0.99999)
        bAvg = ((totalFrameOfVideo * bAvg) + (1 * B)) / (totalFrameOfVideo + 0.99999)
    totalFrameOfVideo+=1
print('Frame height: '+str(len(rAvg)))
print('Frame width: '+str(len(rAvg[0])))
print('Total frame: '+str(totalFrameOfVideo))
# Hợp nhất các giá trị trung bình RGB với nhau
avg=cv2.merge([bAvg, gAvg, rAvg]).astype('uint8')
cv2.imwrite(args['output'], avg)
stream.release()
print('[INFO] Success!!!')