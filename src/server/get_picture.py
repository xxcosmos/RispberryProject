import numpy as np
import cv2
from PyQt5.QtGui import QImage


class GetPicture(object):
    def cvMat2QImage(self,mat):
        img_rgb = cv2.cvtColor(mat,cv2.COLOR_BGR2BGRA)
        return QImage(img_rgb.data,img_rgb.shape[1],img_rgb.shape[0],QImage.Format_RGB32)

    def streaming(connection, stream_bytes=b' '):
        stream_bytes += connection.read(1024)
        first = stream_bytes.find(b'\xff\xd8')
        last = stream_bytes.find(b'\xff\xd9')
        if first != -1 and last != -1:
            jpg = stream_bytes[first:last + 2]
            stream_bytes = stream_bytes[last + 2:]
            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('image',image)
            return stream_bytes, image
        else:
            return b' ', None
