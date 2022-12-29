import cv2, json
import numpy as np
from redis import Redis


class RedisQueue(Redis):
    """
        Redis Lists are an ordered list, First In First Out Queue
        Redis List pushing new elements on the head (on the left) of the list.
        The max length of a list is 4,294,967,295
    """
    def __init__(self, **redis_kwargs):
        super().__init__(**redis_kwargs)

    def size(self, key):  # 큐 크기 확인
        return self.llen(key)

    def is_empty(self, key):  # 비어있는 큐인지 확인
        return self.size(key) == 0

    def put(self, key, element):  # 데이터 넣기
        return self.lpush(key, element)  # left push
    
    def put_img_arr(self, key, img_arr, img_ext='.png'):
        _, buffer = cv2.imencode(img_ext, img_arr)
        img_byte = np.array(buffer).tobytes()
        self.put(key, img_byte)

    def put_and_trim(self, key, element, max_size):  # 데이터 넣기
        queue_count = self.lpush(key, element)  # left push
        self.ltrim(key, 0, max_size - 1)  # 최대크기를 초과한 경우 자르기
        return queue_count

    def get(self, key, is_blocking=False, timeout=None):  # 데이터 꺼내기
        if is_blocking:
            element = self.brpop(key, timeout=timeout)  # blocking right pop
            element = element[1]  # key[0], value[1]
        else:
            element = self.rpop(key)  # right pop
        return element
    
    def get_img_arr(self, key):
        img_byte = self.get(key)
        if img_byte is None:
            print('Redis에 데이터가 없습니다.')
            img_arr = None
        else:
            img_arr = cv2.imdecode(np.frombuffer(img_byte, np.uint8), 1)
            
        return img_arr

    # def get_without_pop(self, key):  # 꺼낼 데이터 조회
    #     if self.is_empty(key):
    #         return None
    #     element = self.lindex(key, -1)
    #     return element