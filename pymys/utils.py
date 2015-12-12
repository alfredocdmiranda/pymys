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
