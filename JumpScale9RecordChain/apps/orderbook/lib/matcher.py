
from js9 import j
from json import loads
from orderbook.lib.orderbuy import OrderBuy
from orderbook.lib.ordersell import OrderSell
import gevent

JSBASE = j.application.jsbase_get_class()


class Matcher(JSBASE,):
    
    def run(self):
        while(True):
            gevent.sleep(20)
            self.logger.info("Matching started")
            sell_list = OrderSell().list(wallet=None)
            buy_list = OrderBuy().list(wallet=None)
            self.match(sell_list, buy_list)

    def match(self, sell_list, buy_list):
        """ matching sell orders with buy orders and generating commands for trader
        it will match using price time priority Algorithm which means
        Orders with better prices (minimum sell or maximum buy) fullfilled first
        that's why it's very important to pass sorted lists in parameters

        :param sell_list: list of sell orders SORTED incremental
        :type sell_list: list of orders
        :param buy_list: list of buy orders SORTED decrementaly
        :type buy_list: list of orders
        """
        current_sell_index = 0
        # a deadlock happens when the biggest price_max for buy orders is
        # less taht the smallest price_min for sell orders
        # or when we run out of sell orders
        dead_lock = False
        for buy_order in buy_list:
            # self.visualize_lists(sell_list, buy_list)
            if dead_lock:
                break
            fulfillled = False
            while not fulfillled:
                if len(sell_list) > current_sell_index: 
                    sell_order = sell_list[current_sell_index]
                    if sell_order['price_min_usd'] <= buy_order['price_max_usd']:
                        trade_amount = 0
                        if sell_order['amount'] == buy_order['amount']:
                            trade_amount = sell_order['amount']
                            buy_order['amount'] = 0
                            sell_order['amount'] = 0
                            current_sell_index += 1
                            fulfillled = True
                        elif sell_order['amount'] < buy_order['amount']:
                            trade_amount = sell_order['amount']
                            buy_order['amount'] -= sell_order['amount']
                            sell_order['amount'] = 0
                            current_sell_index += 1
                        elif sell_order['amount'] > buy_order['amount']:
                            trade_amount = buy_order['amount']
                            sell_order['amount'] -= buy_order['amount']
                            buy_order['amount'] = 0
                            fulfillled = True
                        #TODO: send command to trader
                        self.logger.info("sending {}{}".format(trade_amount, sell_order['currency_to_sell']))
                    else:
                        self.logger.info("order can't be matched min_price for sell = {} and the max_price for buy ={}"
                            .format(sell_order['price_min'], buy_order['price_max']))
                        dead_lock = True
                        break

                else:
                    self.logger.warning("no sell orders to fullfill")
                    dead_lock = True
                    break
        # self.visualize_lists(sell_list, buy_list)
    
    def test(self):
        buy_list, sell_list = self.test_data
        self.match(sell_list, buy_list)
    
    @property
    def test_data(self):
        sell_list = [
            {
                "comment": "",
                "currency_to_sell": "TFT",
                "amount": 14,
                "currency_accept" : ['BTC'],
                "price_min": 10,           
                "expiration": 0,
                "sell_to": None,
                "secret": None
            },
            {
                "comment": "",
                "currency_to_sell": "TFT",
                "amount": 40,
                "currency_accept" : ['BTC'],
                "price_min": 10,           
                "expiration": 0,
                "sell_to": None,
                "secret": None
            },
            {
                "comment": "",
                "currency_to_sell": "TFT",
                "amount": 60,
                "currency_accept" : ['BTC'],
                "price_min": 11,           
                "expiration": 0,
                "sell_to": None,
                "secret": None
            },
            {
                "comment": "",
                "currency_to_sell": "TFT",
                "amount": 65,
                "currency_accept" : ['BTC'],
                "price_min": 11,           
                "expiration": 0,
                "sell_to": None,
                "secret": None
            },
            {
                "comment": "this min price is bigger than any max price of any buy order",
                "currency_to_sell": "TFT",
                "amount": 48,
                "currency_accept" : ['BTC'],
                "price_min": 100,           
                "expiration": 0,
                "sell_to": None,
                "secret": None
            },
        ]
        buy_list = [
            {
                "comment": "",
                "currency_to_buy": "TFT",
                "currency_mine": "BTC",
                "amount": 21,
                "price_max": 15,
                "expiration": 0,
                "buy_from": None,
                "secret": ""
            },
            {
                "comment": "",
                "currency_to_buy": "TFT",
                "currency_mine": "BTC",
                "amount": 16,
                "price_max": 15,
                "expiration": 0,
                "buy_from": None,
                "secret": ""
            },
            {
                "comment": "",
                "currency_to_buy": "TFT",
                "currency_mine": "BTC",
                "amount": 100,
                "price_max": 15,
                "expiration": 0,
                "buy_from": None,
                "secret": ""
            }
            
        ]
        return buy_list, sell_list
    
    def visualize_lists(self, sell_orders, buy_orders):
        print("TYPE\t AMOUNT\t PRICE")
        for sell_order in sell_orders:
            print("SELL\t {}\t {}".format(sell_order['amount'], sell_order['price_min']))
        for buy_order in buy_orders:
            print("BUY\t {}\t {}".format(buy_order['amount'], buy_order['price_max']))

if __name__ == "__main__":
    Matcher('test').test()