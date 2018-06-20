from js9 import j

class OrderBuy(object):
    @classmethod
    def add(cls, wallet, order):
        """
        Add buy order

        :param order: Selling Order
        :type order: !threefoldtoken.order.sell
        :param wallet: Cuurent wallet
        :type wallet: !threefoldtoken.wallet
        :return: Order ID
        :rtype: int
        """
        order.owner_email_addr = wallet.email
        order.wallet_addr = wallet.addr

        id = j.servers.gedis2.latest.context['buy_orders_id'].get()

        j.servers.gedis2.latest.db.tables['orderbuy'].set(id=id, data=order.data)

        # You can add data to db also using
        # data = j.data.serializer.msgpack.dumps([id, order.data])
        # j.servers.gedis2.latest.models.threefoldtoken_order_buy.set(data)

        j.servers.gedis2.latest.context['buy_orders'][id] = order
        return id

    @staticmethod
    def update(wallet, order):
        """
        Update buy order

        :param wallet: Cuurent wallet
        :param order: Selling Order
        :type order: !threefoldtoken.order.sell
        :type wallet: !threefoldtoken.wallet
        """
        if order.id in j.servers.gedis2.latest.context['buy_orders']:
            old_order = j.servers.gedis2.latest.context['buy_orders'][order.id]

            if old_order.wallet_addr != wallet.addr:
                raise RuntimeError('Not authorized')

            order.owner_email_addr = wallet.email
            order.wallet_addr = wallet.addr

            j.servers.gedis2.latest.db.tables['orderbuy'].set(id=order.id, data=order.data)
            j.servers.gedis2.latest.context['buy_orders'][order.id] = order
            return order.id
        else:
            raise RuntimeError('not found')

    @classmethod
    def remove(cls, wallet, id):
        """
        Remove Buy order

        :param wallet: Cuurent wallet
        :type wallet: !threefoldtoken.wallet
        :param id: Buy order id
        :rtype id: int
        """
        if id in j.servers.gedis2.latest.context['buy_orders']:
            order = j.servers.gedis2.latest.context['buy_orders'][id]
            if order.wallet_addr != wallet.addr:
                raise RuntimeError('Not authorized')
            j.servers.gedis2.latest.context['buy_orders'].pop(id)
            return id
        else:
            raise RuntimeError('not found')

    @classmethod
    def list(cls, wallet, id='*'):
        """
        List / Filter Buy order in current user wallet

        :param wallet: Cuurent wallet
        :type wallet: !threefoldtoken.wallet
        :return: List of buy orders
        :rtype: list
        """
        cached_orders = orders = list(j.servers.gedis2.latest.context['buy_orders'].values())

        if id != '*':
            res = j.servers.gedis2.latest.db.tables['orderbuy'].find(id=id)
            return [o for o in res if o.id in orders and o.wallet_addr == wallet.addr]
        else:
            res= [o.ddict for o in cached_orders if o.wallet_addr == wallet.addr]
            return res

    @classmethod
    def get(cls, wallet, id):
        """
          get a Buy order by ID

          :param wallet: Cuurent wallet
          :type wallet: !threefoldtoken.wallet
          :param id: buy order id
          :rtype id: int
          """
        if id in j.servers.gedis2.latest.context['buy_orders']:
            order = j.servers.gedis2.latest.context['buy_orders'][id]
            if order.wallet_addr != wallet.addr:
                raise RuntimeError('Not authorized')
            return j.servers.gedis2.latest.context['buy_orders'].get(id)
        raise RuntimeError('not found')