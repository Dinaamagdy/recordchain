import threading
from orderbook.iyo import Iyo

import uuid
from js9 import j

JSBASE = j.application.jsbase_get_class()

class order_book(JSBASE):
    """
    This class functions are actually registered in

    """
    def __init__(self):
        JSBASE.__init__(self)
        self.wallet = None
        self.iyo = Iyo()
        j.servers.gedis2.latest.globals = {
            'buy_orders': {},
            'sell_orders':{},
            'wallets': {},
            'buy_orders_idx_lock' : threading.Lock(),
            'sell_orders_idx_lock': threading.Lock(),
            'buy_orders_idx' : 0,
            'sell_orders_idx': 0,
            'matching_lock': threading.Lock()
        }

        self.buy_orders = j.servers.gedis2.latest.globals['buy_orders']
        self.sell_orders = j.servers.gedis2.latest.globals['buy_orders']
        self.wallets = j.servers.gedis2.latest.globals['wallets']

        self.buy_orders_idx_lock = j.servers.gedis2.latest.globals['buy_orders_idx_lock']
        self.sell_orders_idx_lock = j.servers.gedis2.latest.globals['sell_orders_idx_lock']
        self.buy_orders_idx = j.servers.gedis2.latest.globals['buy_orders_idx']
        self.sell_orders_idx = j.servers.gedis2.latest.globals['sell_orders_idx']

        self.matching_lock = j.servers.gedis2.latest.globals['matching_lock']

    ##################################################
    # Functions start with _ are not exposed to client
    ##################################################

    def _check_wallet(self):
        """
        Check user is logged in using `wallet_register` command
        """
        if not self.wallet:
            raise RuntimeError('Wallet not registered')

    def _get_id(self, order='sell'):
        """
        Get Next Order ID
        """
        if order=='sell':
            lock = self.sell_orders_idx_lock
        else:
            lock = self.buy_orders_idx_lock

        try:
            lock.acquire()
            if order == 'sell':
                self.sell_orders_idx += 1
                return self.sell_orders_idx
            else:
                self.buy_orders_idx += 1
                return self.buy_orders_idx
        finally:
            lock.release()

    ########################
    # EXPOSED API TO client
    ########################

    def wallet_register(self,addr,jwt,ipaddr,schema_out):
        """
        ```in
        addr = "" (S)
        jwt = "" (S)  
        ipaddr = "" (S)
        ```
        ```out
        !threefoldtoken.wallet
        ```
        """
        user = self.iyo.verify(jwt)

        if not user:
            raise RuntimeError('Invalid JWT')

        self.wallet = schema_out.new()
        self.wallet.ipaddr = ipaddr
        self.wallet.addr = addr
        self.wallet.jwt = jwt
        self.wallet.email = user['email']
        return self.wallet

    def add_sell_order(self,order):
        """
        ```in
        !threefoldtoken.order.sell     
        ```
        """
        self._check_wallet()
        order.owner_email_addr = self.wallet.email
        id = self._get_id(order='sell')
        data = j.data.serializer.msgpack.dumps([id, order.data])
        j.servers.gedis2.latest.models.threefoldtoken_order_sell.set(data)
        self.sell_orders[id] = order
        return id

    def add_buy_order(self,order):
        """
        ```in
        !threefoldtoken.order.buy     
        ```
        """
        self._check_wallet()
        order.owner_email_addr = self.wallet.email
        id = self._get_id(order='buy')
        data = j.data.serializer.msgpack.dumps([id, order.data])
        j.servers.gedis2.latest.models.threefoldtoken_order_buy.set(data)
        self.buy_orders[id] = order
        return id

    def remove_sell_order(self, order_id):
        """
        ```in
        order_id = (I)
        ```
        """
        self._check_wallet()
        try:
            self.matching_lock.acquire()
            if order_id in self.sell_orders:
                if self.sell_orders[order_id].owner_email_addr == self.wallet.email:
                    self.sell_orders.pop(order_id)
                    return True
            return False
        finally:
            self.matching_lock.release()

    def remove_buy_order(self, order_id):
        """
        ```in
        order_id = (I)
        ```
        """
        self._check_wallet()
        try:
            self.matching_lock.acquire()
            if order_id in self.buy_orders:
                if self.buy_orders[order_id].owner_email_addr == self.wallet.email:
                    self.buy_orders.pop(order_id)
                    return True
            return False
        finally:
            self.matching_lock.release()

    def get_sell_order(self, order_id, schema_out):
        """
        ```in
        order_id = (I)
        ```
        ```out
        !threefoldtoken.order.sell
        ```
        """
        self._check_wallet()
        if order_id in self.sell_orders:
            order = self.sell_orders[order_id]
            order = schema_out.get(capnpbin=order.data)
            if order.owner_email_addr != self.wallet.email:
                order.owner_email_addr = ""
            return order
        raise RuntimeError('not-found')

    def get_buy_order(self, order_id, schema_out):
        """
        ```in
        order_id = (I)
        ```
        ```out
        !threefoldtoken.order.buy
        ```
        """
        self._check_wallet()
        if order_id in self.buy_orders:
            order = self.buy_orders[order_id]
            order = schema_out.get(capnpbin=order.data)
            if order.owner_email_addr != self.wallet.email:
                order.owner_email_addr = ""
            return order
        raise RuntimeError('not-found')

    def list_sell_orders(self, schema_out):
        """
        ```out
        orders = (LO) !threefoldtoken.order.sell
        ```
        """
        result = schema_out.new()

        s = j.data.schema.schema_from_url('threefoldtoken.order.sell')
        for id, order in self.sell_orders.items():
            order = s.get(capnpbin=order.data)
            order.owner_email_addr = ""
            result.orders.append(order)
        return result
    #
    # def list_buy_orders(self):
    #     result = []
    #     s = j.data.schema.schema_from_url('threefoldtoken.order.buy')
    #     for order in self.buy_orders:
    #         order = s.new().get(capnpbin=order.data)
    #         order.owner_email_addr = ""
    #         result.append(order)
    #     return result
    #
    # def update_sell_order(self, id, order, schema_out):
    #     """
    #     ```in
    #     id = (N)
    #     order = (O) !threefoldtoken.order.sell
    #     ```
    #     ```out
    #     !threefoldtoken.order.sell
    #     ```
    #     """
    #     self._check_wallet()
    #     try:
    #         if id in self.sell_orders:
    #             self.matching_lock.acquire()
    #             data = j.data.serializer.msgpack.dumps([id, order.data])
    #             j.servers.gedis2.latest.models.threefoldtoken_order_sell.set(data)
    #             self.buy_orders[id] = order
    #             return True
    #         return False
    #     finally:
    #         self.matching_lock.release()
    #
    # def update_buy_order(self, id, order, schema_out):
    #     """
    #     ```in
    #     id = (N)
    #     order = (O) !threefoldtoken.order.buy
    #     ```
    #     ```out
    #     !threefoldtoken.order.buy
    #     """
    #     self._check_wallet()
    #     try:
    #         if id in self.buy_orders:
    #             self.matching_lock.acquire()
    #             data = j.data.serializer.msgpack.dumps([id, order.data])
    #             j.servers.gedis2.latest.models.threefoldtoken_order_buy.set(data)
    #             self.buy_orders[id] = order
    #             return True
    #         return False
    #     finally:
    #         self.matching_lock.release()

    def order_buy_match(self,order_id, schema_out):
        self._check_wallet()
        pass

