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
        o = j.data.schema.schema_from_url('threefoldtoken.order.buy').new()
        o.copy_from(order)
        o.owner_email_addr = wallet.email
        o.wallet_addr = wallet.addr
        id = j.servers.gedis2.latest.context['buy_orders_id'].get()
        o.id = id
        j.servers.gedis2.latest.db.tables['orderbuy'].set(id=id, data=o.data)

        # You can add data to db also using
        # data = j.data.serializer.msgpack.dumps([id, order.data])
        # j.servers.gedis2.latest.models.threefoldtoken_order_buy.set(data)

        j.servers.gedis2.latest.context['buy_orders'][id] = o
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
        id = order.id

        if id not in j.servers.gedis2.latest.context['buy_orders']:
            raise RuntimeError('not found')

        old_order = j.servers.gedis2.latest.context['buy_orders'][id]

        if old_order.wallet_addr != wallet.addr:
            raise RuntimeError('Not authorized')

        if old_order.approved:
            raise RuntimeError('Order is locked. No more updates are possible')

        o = j.data.schema.schema_from_url('threefoldtoken.order.buy').new()
        o.copy_from(order)

        o.owner_email_addr = wallet.email
        o.wallet_addr = wallet.addr
        j.servers.gedis2.latest.db.tables['orderbuy'].set(id=id, data=o.data)
        j.servers.gedis2.latest.context['buy_orders'][id] = o
        return id

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
            if order.approved:
                raise RuntimeError('Order is locked. can not be deleted')
            j.servers.gedis2.latest.context['buy_orders'].pop(id)
            return id
        else:
            raise RuntimeError('not found')

    @classmethod
    def list(cls, wallet=None, sortby='id', desc=False, **kwargs):
        """
        List / Filter Buy orders
        If wallet is provided, get user orders only
        If wallet is None, retrieve all orders

        :param wallet: Cuurent wallet
        :type wallet: !threefoldtoken.wallet
        :param sortby: field to sort with
        :type sortby: str
        :param desc: Descending order
        :type desc: bool
        :param kwargs: filter result according to the provided value for a given field
        :return: List of buy orders
        :rtype: list
        """
        orders = []

        for k, v in j.servers.gedis2.latest.context['buy_orders'].items():
            # Filter only orders belonging to certain wallet if provided
            if wallet is not None and v.wallet_addr != wallet.addr:
                continue

            # filter only orders matching the passed kwargs filters (exact values)
            valid = True
            for field, value in kwargs.items():
                if hasattr(field, value) and getattr(v, field) != value:
                    valid = False
                    break
            if valid:
                orders.append(v)
        if not sortby:
            orders.sort(key=lambda x: x.id, reverse=desc)
        else:
            def sort_func(order):
                return getattr(order, sortby)
            orders.sort(key=sort_func, reverse=desc)
        return orders

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
            order.id = id
            return order
        raise RuntimeError('not found')
