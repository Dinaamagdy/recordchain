from js9 import j


class Transaction:
    @classmethod
    def new(self, sell_order_id, buy_order_id, amount, currency, price):
        transaction = j.data.schema.schema_from_url('threefoldtoken.transaction').new()
        transaction.sell_order_id = sell_order_id
        transaction.buy_order_id = buy_order_id
        transaction.amount_bought = amount
        transaction.currency = currency
        transaction.total_price = price

        return transaction