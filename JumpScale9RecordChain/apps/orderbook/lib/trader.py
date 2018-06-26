from js9 import j
from gevent.event import Event
from queue import Queue
import gevent

JSBASE = j.application.jsbase_get_class()


class Trader(JSBASE):
    """
   Trader (Do transactions)
    """
    def __init__(self):
        """
        Trader
        """
        JSBASE.__init__(self)
        self.queue = Queue()
        self.evt = Event()
        g = gevent.spawn(self._consume)
        g.start()

    def put(self, transactions):
        """
        Put all transactions coming from a run round of the matcher
        to be processed

        :param transactions: list of transactions coming from trader
        :type transactions: list
        """
        for transaction in transactions:
            self.queue.put(transaction)

        # Now notify consumer to consume these transactions
        self.evt.set()
        gevent.sleep(0)
        self.evt.clear()

    def _post_success(self, transaction):
        """
        Actions to take if transaction succeeded
        like save to db

        :param transaction: transaction
        :type transaction: !threefoldtoken.transaction
        """
        # @TODO: remove orders with 0- amounts from matcher
        self.logger.info("Succeeded transaction")
        print(transaction)

    def _post_failure(self, transaction):
        """
        Actions to take if transaction fails
        like undo transaction in matcher list

        :param transaction: transaction
        :type transaction: !threefoldtoken.transaction
        """
        # @TODO: undo transaction in matcher lists
        self.logger.info("failed transaction")
        print(transaction)

    def process(self, transaction):
        """
        Process transaction
        if succeeded, save to db
        if failed, undo transaction in list of approved orders
        :param transaction:
        :return:
        """
        # @TODO: Actual transaction logic
        success = True

        if success:
            self._post_success(transaction)
        else:
            self._post_failure(transaction)

    def _consume(self):
        """
        consume queue, and process transactions
        """
        while True:
            if not self.queue.empty():
                transaction = self.queue.get()
                self.process(transaction)
            else:
                self.logger.info("Waiting for transactions to come")
                self.evt.wait()
                gevent.sleep(0)


if __name__ == '__main__':
    t = Trader()
    t.put([1,2,3,4,5,6])
    t.put([1, 2, 3, 4, 5, 6])
    t.put([1, 2, 3, 4, 5, 6])
