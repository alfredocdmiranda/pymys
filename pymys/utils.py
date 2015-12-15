import re
import time
from queue import Queue
from threading import Lock


class IndexableQueue(Queue):
    def __getitem__(self, index):
        with self.mutex:
            return self.queue[index]


class DictThreadSafe(dict):
    def __init__(self, *args, **kwargs):
        self.lock = Lock()
        super(DictThreadSafe, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        self.lock.acquire()
        try:
            value = dict.__getitem__(self, key)
        finally:
            self.lock.release()

        return value

    def __setitem__(self, key, value):
        self.lock.acquire()
        dict.__setitem__(self, key, value)
        self.lock.release()


def serial_read(ser, delimiter="\n", timeout=2):
    """
    Every time serial gets read anything from the port, the timeout is restarted.
    :param ser:
    :param delimiter:
    :param timeout:
    :return:
    """
    matcher = re.compile(delimiter)
    buff = ""
    now = time.time()
    while ((time.time() - now) <= timeout) and (not matcher.search(buff)):
        data = ser.read(1)
        if data:
            now = time.time()
            buff += data.decode(encoding='utf-8')

    return buff