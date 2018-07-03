# OrderBook

## Description
- An order book is a ledger containing all pending orders [buy/sell]
- these orders are paired up as soon as their requirements are fulfilled.
- A transaction is issued with each match
- When adding/editing an order, if `approved` field is set to True
no further updates or deletes to this order is possible, and order is
scheduled for matching
- Upon matching, list of possible transactions are created and needed to be executed
- upon failure of transactions, orders eligible for transactions are updated by the result of these transactions

## Needed APIs
- Orders
    - Add
    - update
    - delete
    - list/filter (all/client) orders
    
- Matching
- Trading
- Transactions
    - list/filter (all/client) transactions with tht ability to filter (all/pending/successed/failed) ones

## Goal
- implement an orderbook server(on top of gedis2 server)
- Orders are saved in memory and committed to db for history only

## Deliverables
- Order book server using gedis2 with SSL support
- Python client for orderbook
- Create a matcher to match selling with buying orders
- Create a trader to actually do the transactions to user wallets

## Design
- API layer accessible through gedis2 server
- SAL layer for handling logic (called by API)
- Matcher
- Trader

# Flow

- Client logs in using `JWT` from [It's you online](https://itsyou.online) and wallet info
- Then client can do CRUD opertations on orders
- If client added/updated an order with the field `approved` set to `True` this means order is
no more eligible for further updates and it became eligible to be matched against other
approved orders
- **Matcher** 
    - There's a `Matcher` daemon waiting for approved orders and for each added `approved` order
     it will start matching that order immediately
     
    - Matcher notifies `Trader` then  with a list of possible matches
- **Trader**
    - There's a `Trader` daemon running and waiting to be notified with a list of possible
    transactions
    - For each transaction in these transactions:
        - persisit transaction to DB with state of `pending`
        - Try execute transaction and if failed, update original order back with original amounts of money
   

# Matching algorithm




## Code
[Order book](https://github.com/rivine/recordchain/tree/master/JumpScale9RecordChain/servers/orderbook)

