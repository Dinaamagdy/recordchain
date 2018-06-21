from js9 import j


class OrderSell(object):

    @classmethod
    def add(cls, wallet, order):
        """
        Add Sell order

        :param order: Selling Order
        :type order: !threefoldtoken.order.sell
        :param wallet: Cuurent wallet
        :type wallet: !threefoldtoken.wallet
        :return: Order ID
        :rtype: int
        """
        order = j.data.schema.schema_from_url('threefoldtoken.order.sell').get(capnpbin=order.data)
        order.owner_email_addr = wallet.email
        order.wallet_addr = wallet.addr
        id = j.servers.gedis2.latest.context['sell_orders_id'].get()
        order.id = id
        j.servers.gedis2.latest.db.tables['ordersell'].set(id=id, data=order.data)

        # You can add data to db also using
        # data = j.data.serializer.msgpack.dumps([id, order.data])
        # j.servers.gedis2.latest.models.threefoldtoken_order_sell.set(data)

        j.servers.gedis2.latest.context['sell_orders'][id] = order
        return id

    @staticmethod
    def update(wallet, order):
        """
        Update Sell order

        :param wallet: Cuurent wallet
        :param order: Selling Order
        :type order: !threefoldtoken.order.sell
        :type wallet: !threefoldtoken.wallet
        """
        if order.id in j.servers.gedis2.latest.context['sell_orders']:
            order = j.data.schema.schema_from_url('threefoldtoken.order.sell').get(capnpbin=order.data)
            old_order = j.servers.gedis2.latest.context['sell_orders'][order.id]

            if old_order.wallet_addr != wallet.addr:
                raise RuntimeError('Not authorized')

            order.owner_email_addr = wallet.email
            order.wallet_addr = wallet.addr

            j.servers.gedis2.latest.db.tables['ordersell'].set(id=order.id, data=order.data)
            j.servers.gedis2.latest.context['sell_orders'][order.id] = order
            return order.id
        else:
            raise RuntimeError('not found')

    @classmethod
    def remove(cls, wallet, id):
        """
        Remove Sell order

        :param wallet: Cuurent wallet
        :type wallet: !threefoldtoken.wallet
        :param id: Sell order id
        :rtype id: int
        """
        if id in j.servers.gedis2.latest.context['sell_orders']:
            order = j.servers.gedis2.latest.context['sell_orders'][id]
            if order.wallet_addr != wallet.addr:
                raise RuntimeError('Not authorized')
            j.servers.gedis2.latest.context['sell_orders'].pop(id)
            return id
        else:
            raise RuntimeError('not found')

    @classmethod
    def list(cls, wallet=None, sortby='price_min', desc=False):
        """
        List / Filter Sell order in current user wallet
        If wallet is provided, get user orders only
        If wallet is None, retrieve all orders

        :param wallet: Cuurent wallet
        :type wallet: !threefoldtoken.wallet
        :param sortby: field to sort with
        :type sortby: str
        :param desc: Descending order
        :type desc: bool
        :param exclude_wallet_data: exclude wallet info
        :type exclude_wallet_data: bool

        :return: List of Sell orders
        :rtype: list
        """
        orders = []

        for k, v in j.servers.gedis2.latest.context['sell_orders'].items():
            if wallet is not None:
                if v.wallet_addr == wallet.addr:
                    orders.append(v)
            else:
                orders.append(v)

        if not sortby:
            orders.sort(key=lambda x: x.id, reverse=desc)
        else:
            def sort_func(order):
                return getattr(order, '%s_usd'%sortby)
            orders.sort(key=sort_func, reverse=desc)

        res = []

        for order in orders:
            d = order.ddict_hr
            if wallet is None:
                d['owner_email_addr'] = ''
                d['wallet_addr'] = ''
            res.append(d)

        return res

    @classmethod
    def get(cls, wallet, id):
        """
          get a Sell order by ID

          :param wallet: Cuurent wallet
          :type wallet: !threefoldtoken.wallet
          :param id: Sell order id
          :rtype id: int
          """
        if id in j.servers.gedis2.latest.context['sell_orders']:
            order = j.servers.gedis2.latest.context['sell_orders'][id]
            if order.wallet_addr != wallet.addr:
                raise RuntimeError('Not authorized')
            return j.servers.gedis2.latest.context['sell_orders'].get(id)
        raise RuntimeError('not found')
