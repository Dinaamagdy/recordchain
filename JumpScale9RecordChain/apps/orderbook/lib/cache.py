from queue import Queue


class Id(object):
    def __init__(self):
        self.queue = Queue()
        self._populate(1)

    def get(self):
        idx = self.queue.get()
        if self.queue.empty():
            self._populate(idx+1)
        return idx

    def _populate(self, start_from, count=10000):
        for i in range(start_from, start_from+count):
            self.queue.put(i)

