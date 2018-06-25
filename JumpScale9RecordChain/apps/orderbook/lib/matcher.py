
from js9 import j
from json import loads
import cryptocompare
from orderbook.lib.orderbuy import OrderBuy
from orderbook.lib.ordersell import OrderSell
import gevent

JSBASE = j.application.jsbase_get_class()
Numeric = j.data.types.numeric
Date = j.data.types.date

class Matcher(JSBASE,):
    
    def run(self):
        """starts matching every 5 seconds
        this should be spawned by gevent
        
        """

        while(True):
            gevent.sleep(5)
            self.logger.info("Matching started")
            sell_list = OrderSell().list(wallet=None)
            buy_list = OrderBuy().list(wallet=None)
            self.match(sell_list, buy_list)

    def match(self, sell_list, buy_list):
        """executes matching between list of sell orders and a list of buy orders
        will compare eache buy order againest all sell orders
        
        :param sell_list: list of sell orders
        :type sell_list: list
        :param buy_list: list of buy orders
        :type buy_list: list
        """

        
        sell_list = self.toDict(sell_list)
        buy_list = self.toDict(buy_list)

        for buy_order in buy_list:
            buy_price_str = buy_order['price_max']
            fulfilled = False
            while not fulfilled:
                self.visualize_lists(sell_list, buy_list)
                best_sell = None
                best_sell_index = None
                for index, sell_order in enumerate(sell_list):
                    if self.is_valid(sell_order, buy_order):
                        if best_sell == None:
                            best_sell = sell_order
                            best_sell_index = index
                        else:
                            best_sell_price = best_sell['price_min']
                            current_sell_price = sell_order['price_min']
                            if currencies_compare(best_sell_price, sell_price_str) == 1: # if the best sell price is bigger than the current sell price
                                best_sell = sell_order
                                best_sell_index = index
                    else:
                        continue

                if best_sell:
                    trade_amount = 0
                    if best_sell['amount'] == buy_order['amount']:
                        trade_amount = best_sell['amount']
                        buy_order['amount'] = 0
                        del sell_list[best_sell_index]
                        fulfilled = True
                    elif best_sell['amount'] < buy_order['amount']:
                        trade_amount = best_sell['amount']
                        buy_order['amount'] -= best_sell['amount']
                        del sell_list[best_sell_index]
                    elif best_sell['amount'] > buy_order['amount']:
                        trade_amount = buy_order['amount']
                        sell_list[best_sell_index]['amount'] -= buy_order['amount']
                        buy_order['amount'] = 0
                        fulfilled = True
                    #TODO: send command to trader
                    self.logger.info("sending {}{}".format(trade_amount, best_sell['currency_to_sell']))
                else:
                    break

    def currencies_compare(self, currency1, currency2):
        """compares two string representations of currency
        if both parameters of the same currency it will directly compare values
        otherwise the second parameter will be be converted to the first parameter currency first
        Example:
        self.currencies_compare("10.0 EUR", "10.0 USD")
        
        :param currency1: string reprentation of currency1
        :type currency1: string
        :param currency2: string reprentation of currency1
        :type currency2: string

        :return 
        0 means equal
        1 greater than
        -1 less than
        """
        currency1_value ,currency1_currency = Numeric.getCur(currency1)
        currency2_value ,currency2_currency = Numeric.getCur(currency2)

        if currency1_currency != currency2_currency:
            price = cryptocompare.get_price(currency2_currency, currency1_currency)
            currency2_value = currency2_value * price
            currency2_currency = currency1_currency

        # its safe now to compare value
        if currency1_value == currency2_value:
            return 0
        elif currency1_value < currency2_value:
            return -1
        elif currency1_value > currency2_value:
            return 1

    def is_valid(self, sell_order, buy_order):
        """this method checks if the two orders can be matched or not according the following
        1- check expiration for both orders
        2- check if these orders have secrets, and validate these secrets
        3- check if these orders have the same currencies targeted
        4- check if the price_max for the buy order is greater than or equal price_min for sell order 
        
        :param sell_order: sell order
        :type sell_order: dict
        :param buy_order: buy order
        :type buy_order: dict
        """
        now = j.data.time.epoch
        if Date.fromString(sell_order['expiration']) < now or Date.fromString(buy_order['expiration']) < now:
            return False
        
        if len(sell_order['secret']) > 0 or len(buy_order['secret']) > 0:
            if not buy_order['secret'] in buy_order['secret']:
                return False
        
        interesection = set(sell_order['currency_accept']) & set(buy_order['currency_mine']) #if not none means that the buyer accepts one of the seller's currencies
        if sell_order['currency_to_sell'] != buy_order['currency_to_buy'] or not interesection:
            return False

        if self.currencies_compare(sell_order['price_min'], buy_order['price_max']) == 1:
            return False

        return True


    def toDict(self, data):
        """converts list of DBModels to list of dicts
        """

        ret = []
        for item in data:
            ret.append(item.ddict_hr)
        return ret
    
    def visualize_lists(self, sell_orders, buy_orders):
        print("TYPE\t AMOUNT\t PRICE")
        for sell_order in sell_orders:
            print("SELL\t {}\t {}".format(sell_order['amount'], sell_order['price_min']))
        for buy_order in buy_orders:
            print("BUY\t {}\t {}".format(buy_order['amount'], buy_order['price_max']))
