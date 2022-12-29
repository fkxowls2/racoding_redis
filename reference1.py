from redis_queue import RedisQueue
import json, time



max_data = 100000
host = 'localhost'
port = 6379


def put_raw_data_to_queue(_data):
    if type(_data) is dict:
        raw_data = json.dumps(_data)
    else:
        raw_data = _data
    q = RedisQueue('raw-data', max_data, host=host, port=port, db=0)
    q_count = q.put(raw_data)
    return q_count


def get_translated_data_from_queue():
    # q = RedisQueue('translated-data', max_data, host=host, port=port, db=0)
    q = RedisQueue('raw-data', max_data, host=host, port=port, db=0)
    terminate_count = int(0.5 * 60 * 5)
    while True:
        if not q.is_empty():
            translated_data = q.get()
            return translated_data
        time.sleep(0.2)
        terminate_count -= 1
        if terminate_count < 1:
            break


def get_json_data_from_queue():
    translated_data = get_translated_data_from_queue()
    if type(translated_data) is bytes:
        return json.loads(translated_data)
    return translated_data