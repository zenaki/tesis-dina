# pip install flask

import os, time, cv2
import numpy as np
import redis, struct
from base_camera import BaseCamera

class Camera(BaseCamera):

    def __init__(self):
        super(Camera, self).__init__()

    @staticmethod
    def fromRedis(r,n):
        """Retrieve Numpy array from Redis key 'n'"""
        encoded = r.get(n)
        h, w = struct.unpack('>II',encoded[:8])
        a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
        return a

    @staticmethod
    def frames():
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        while True:
            frame = Camera.fromRedis(r,'image')
            ret, jpeg = cv2.imencode('.jpg', frame)

            yield (jpeg.tobytes())

