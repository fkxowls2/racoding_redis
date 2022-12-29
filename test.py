from redis_queue import RedisQueue
import cv2, time, datetime
import matplotlib.pyplot as plt
import numpy as np


r = RedisQueue(host='localhost', port=6379, db=0)

idx = 1
while True:
    redis_img_byte = r.get('raw-data')
    if redis_img_byte == None:
        continue
    decoded = cv2.imdecode(np.frombuffer(redis_img_byte, np.uint8), 1)
    cv2.imwrite(f'{str(idx)}.png', decoded)
    print(idx)
    idx += 1