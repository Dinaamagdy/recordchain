from js9 import j


class Transactions:
    def __init__(self):
        self.schema = j.data.schema.schema_from_url('threefoldtoken.transaction')
        self.trader = j.servers.gedis2.latest.context['trader']
        self.transactions = j.servers.gedis2.latest.context['transactions']
    
    def list(self, **kwargs):
        """List / Filter active transactions in the trader
        :param ddict_hr: return data as list of dicts
        :type ddict_hr: bool

        """
        transactions = []
        for transaction in self.transactions:
            for field, value in kwargs.items():
                if transaction.get(field, None) != value:
                    break
            else:
                transactions.append(transaction)

        return transactions

    @classmethod
    def new(self, sell_order_id, buy_order_id, amount, currency, price, state='new'):
        transaction = j.data.schema.schema_from_url('threefoldtoken.transaction').new()
        transaction.sell_order_id = sell_order_id
        transaction.buy_order_id = buy_order_id
        transaction.amount_bought = amount
        transaction.currency = currency
        transaction.total_price = price
        transaction.state = state

        return transaction