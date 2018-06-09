from orderbook.iyo import Iyo

from js9 import j

JSBASE = j.application.jsbase_get_class()

class Wallet():
    
    def __init__(self):
        self.addr = ""
        self.email = ""
        self.jwt = ""


class OrderBook(object):
    def __init__(self):
        self.wallet = None
        self.iyo = Iyo()

    @property
    def buy_orders(self):
        if not 'buy_orders' in j.servers.gedis2.latest.globals:
            j.servers.gedis2.latest.globals['buy_orders'] = []
        return j.servers.gedis2.latest.globals['buy_orders']

    @property
    def sell_orders(self):
        if not 'sell_orders' in j.servers.gedis2.latest.globals:
            j.servers.gedis2.latest.globals['sell_orders'] = []
        return j.servers.gedis2.latest.globals['sell_orders']

    def verify_jwt(self, jwt):
        self.iyo.verify(jwt)


    def add_buy_order(self, order):
        self.buy_orders.append(order)

    def sell_order(self, order):
        self.sell_order.append(order)




class order_book(JSBASE):
    """
    This class functions are actually registered in

    """
    def __init__(self):
        JSBASE.__init__(self)
        self.proxy = OrderBook()

    def wallet_register(self,addr,jwt,ipaddr,schema_out):
        """
        ```in
        addr = "" (S)
        jwt = "" (S)  
        ipaddr = "" (S)
        ```
        """        
        self.proxy.wallet = Wallet()
        self.proxy.wallet.addr = addr
        self.proxy.wallet.jwt = jwt
        self.proxy.wallet.verify()

    def order_sell_register(self,order,schema_out):
        """
        ```in
        !threefoldtoken.order.sell     
        ```
        ```out
        !threefoldtoken.order.sell     
        ```
        
        """
        o = schema_out.new()  #TODO:*1 fix
        return o

    def order_buy_register(self,order,schema_out):
        """
        ```in
        !threefoldtoken.order.buy     
        ```
        ```out
        !threefoldtoken.order.buy     
        ```
        
        """
        o = schema_out.new()  #TODO:*1 fix
        return o

    def order_buy_match(self,order_id, schema_out):
        pass

    def get_jwt(self, iyo_id, iyo_secret):
        """
        Use It's you online ID & Secret to get JWT

        ```in
        iyo_id = "" (S)
        iyo_secret = (S)
        ```
        """
        return self.proxy.iyo.get_jwt(iyo_id, iyo_secret)

    def verify_jwt(self, jwt):
        """

        ```in
        jwt = "" (S)
        ```
        """
        return self.proxy.iyo.verify(jwt)


