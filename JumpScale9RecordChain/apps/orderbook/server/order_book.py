from orderbook.lib.orderbook import OrderBook
from orderbook.lib.idgen import SellOrderIDGenerator, BuyOrderIDGenerator
from orderbook.lib.matcher import Matcher
import gevent 
from js9 import j


JSBASE = j.application.jsbase_get_class()


class order_book(JSBASE):
    """
    This class functions are actually registered in

    """
    def __init__(self):
        JSBASE.__init__(self)
        self.orderbook = OrderBook()

        if not hasattr(j.servers.gedis2.latest, 'context'):
            j.servers.gedis2.latest.context = {
                'wallets': {},
                'sell_orders':{},
                'buy_orders': {},
                'sell_orders_id': SellOrderIDGenerator(max_queue_size=10000),
                'buy_orders_id': BuyOrderIDGenerator(max_queue_size=10000),
                'matcher': Matcher()
            }
            gevent.spawn(j.servers.gedis2.latest.context['matcher'].run)

    def login(self, wallet, schema_out):
        """
        ```in
        !!threefoldtoken.wallet
        ```

        ```out
        !threefoldtoken.wallet
        ```

        Verifies JWT and registers user wallet!

        :param jwt: JWT from Itsyouonline
        :param wallet_addr: Wallet address
        :param wallet_ipaddr: Wallet Ip address
        :param schema_out: !threefoldtoken.wallet
        :return: Wallet
        :rtype: !threefoldtoken.wallet
        """
        w = schema_out.new()
        w.ipaddr = wallet.ipaddr
        w.addr = wallet.addr
        w.jwt = wallet.jwt
        return self.orderbook.wallet.register(w)

    def add_sell_order(self,order):
        """
        ```in
        !threefoldtoken.order.sell.create
        ```

        Add a selling order

        :param order: Selling Order
        :type order: !threefoldtoken.order.sell
        :return: Order ID
        :rtype: int
        """

        return self.orderbook.sell.add(self.orderbook.wallet.current, order)

    def add_buy_order(self,order):
        """
        ```in
        !threefoldtoken.order.buy.create
        ```

        Add a buying order

        :param order: Buying Order
        :type order: !threefoldtoken.order.buy
        :return: Order ID
        :rtype: int
        """
        return self.orderbook.buy.add(self.orderbook.wallet.current, order)

    def update_sell_order(self, order):
        """"
        ```in
        !threefoldtoken.order.sell.update
        ```

        update a selling order

        :param order: Selling Order
        :type order: !threefoldtoken.order.sell
        :return: Order ID
        :rtype: int
        """
        return self.orderbook.sell.update(self.orderbook.wallet.current, order)

    def update_buy_order(self, order):
        """
        ```in
        !threefoldtoken.order.buy.update
        ```

        update a buying order

        :param order: Buying Order
        :type order: !threefoldtoken.order.buy
        :return: Order ID
        :rtype: int
        """
        return self.orderbook.buy.update(self.orderbook.wallet.current, order)

    def remove_sell_order(self, order_id):
        """
        ```in
        order_id = (I)
        ```

        Remove a selling order

        :param order_id: Selling order id
        :rtype order_id: int
        :return: Order ID
        :rtype int
        """
        return self.orderbook.sell.remove(self.orderbook.wallet.current, order_id)

    def remove_buy_order(self, order_id):
        """
        ```in
        order_id = (I)
        ```

        Remove a buying order

        :param order_id: Buying order id
        :rtype order_id: int
        :return: Order ID
        :rtype int
        """
        return self.orderbook.buy.remove(self.orderbook.wallet.current, order_id)

    def get_sell_order(self, order_id, schema_out):
        """
        ```in
        order_id = (I)
        ```
        ```out
        !threefoldtoken.order.sell
        ```

        Get a selling order

        :param order_id: Selling order id
        :type order_id: int
        :param schema_out: Order
        :type schema_out: !threefoldtoken.order.sell
        :return: order
        :rtype !threefoldtoken.order.sell
        """
        return self.orderbook.sell.get(self.orderbook.wallet.current, order_id)

    def get_buy_order(self, order_id, schema_out):
        """
        ```in
        order_id = (I)
        ```
        ```out
        !threefoldtoken.order.buy
        ```

        Get a buying order

        :param order_id: Buying order id
        :type order_id: int
        :param schema_out: Order
        :type schema_out: !threefoldtoken.order.sell
        :return: order
        :rtype !threefoldtoken.order.buy
        """
        return self.orderbook.buy.get(self.orderbook.wallet.current, order_id)

    def list_my_sell_orders(self, sortby, desc):
        """
        ```in
            sortby = id (S) # Field name to sort with
            desc = (B) # Descending order
        ```

        List Selling orders for current client only
        :return: list of selling orders
        :rtype: list
        """
        return [order.ddict_hr for order in self.orderbook.sell.list(self.orderbook.wallet.current, sortby=sortby, desc=desc)]

    def list_my_buy_orders(self, sortby, desc):
        """
        ```in
            sortby = id (S) # Field name to sort with
            desc = (B) # Descending order
        ```

        List Buy orders for current client only
        :return: list of buying orders
        :rtype: list
        """
        return [order.ddict_hr for order in self.orderbook.buy.list(self.orderbook.wallet.current, sortby=sortby, desc=desc)]

    def list_all_sell_orders(self, sortby, desc):
        """
        ```in
            sortby = id (S) # Field name to sort with
            desc = (B) # Descending order
        ```

        List Selling orders
        :return: list of selling orders
        :rtype: list
        """
        res = []

        for order in self.orderbook.sell.list(None, sortby=sortby, desc=desc):
            item = order.ddict_hr
            item['owner_email_addr'] = ''
            item['wallet_addr'] = ''
            res.append(item)
        return res

    def list_all_buy_orders(self, sortby, desc):
        """
        ```in
            sortby = id (S) # Field name to sort with
            desc = (B) # Descending order
        ```

        List Buy orders
        :return: list of buying orders
        :rtype: list
        """
        res = []

        for order in self.orderbook.buy.list(None, sortby=sortby, desc=desc):
            item = order.ddict_hr
            item['owner_email_addr'] = ''
            item['wallet_addr'] = ''
            res.append(item)
        return res