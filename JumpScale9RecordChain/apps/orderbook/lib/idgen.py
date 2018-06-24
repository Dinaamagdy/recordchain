from js9 import j
from gevent.event import Event
from queue import Queue
import gevent

JSBASE = j.application.jsbase_get_class()


class IDGenerator(JSBASE):
    """
    Sequential ID Generator Parent class
    Based on gevents
    """
    def __init__(self, max_queue_size):
        """

        :param name: Name of the gnerator (used in logging)
        :type name: str
        :param max_queue_size: At any point of time, we should have (max_queue_size) number of ids
        :type max_queue_size: int
        """
        JSBASE.__init__(self)
        self.max_queue_size = max_queue_size
        self.queue = Queue()
        self.evt = Event()
        g = gevent.spawn(self._populate)
        g.start()

    def get(self):
        """
        Get an ID in sequence manner
        notify populator / worker to put new ids when queue size reaches
        half of max_queue_size provided at init time
        :return: ID
        :rtype: int
        """
        if self.queue.qsize() <= round(self.max_queue_size / 2):
            self.evt.set()
            gevent.sleep(0)
            self.evt.clear()

        return self.queue.get()

    def _populate(self):
        """
        Worker, used in gevent to watch and generate ids
        when needed / notified
        :return:
        """
        last = 0
        while True:
            start = last + 1
            if start == 1:
                end = last + self.max_queue_size
            else:
                end = last +  round(self.max_queue_size / 2)

            self.logger.info("START Generating new Ids (%s)-(%s)" % (start, end))
            for i in range(start, end + 1):
                self.queue.put(i)

            last = i

            self.logger.info("End Generating new Ids (%s)-(%s)" % (start, end))
            self.evt.wait()
            gevent.sleep(0)


class SellOrderIDGenerator(IDGenerator):
    def __init__(self, max_queue_size):
        super(SellOrderIDGenerator, self).__init__(max_queue_size=max_queue_size)


class BuyOrderIDGenerator(IDGenerator):
    def __init__(self, max_queue_size):
        super(BuyOrderIDGenerator, self).__init__(max_queue_size=max_queue_size)


if __name__ == '__main__':
    x = SellOrderIDGenerator(5)
    for i in range(50):
        print(x.get())

