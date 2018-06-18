from gevent.queue import Queue


class Id(object):
    def __init__(self):
        self.queue = Queue()
        self.queue.put(1)

    def get(self):
        idx = self.queue.get()
        self.queue.put(idx+1)
        return idx


