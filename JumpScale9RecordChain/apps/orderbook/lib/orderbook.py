from js9 import j

from orderbook.lib.ordersell import OrderSell
from orderbook.lib.orderbuy import OrderBuy
from orderbook.lib.wallet import Wallet
from orderbook.lib.decorators import is_logged_in


class OrderBook(object):

    wallet = Wallet()

    @property
    @is_logged_in
    def buy(self):
        return OrderBuy

    @property
    @is_logged_in
    def sell(self):
        return OrderSell

