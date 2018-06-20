## OrderBook

# Description
- An order book is a ledger containing all pending orders [buy/sell]
- these orders are paired up as soon as their requirements are fulfilled.
- A transaction is issued with each match

## Needed APIs
Create order  
Read orders ( with some filters)   
Delete orders
Matching
Trading


# Goal
- implement an orderbook server(on top of gedis2 server)
- Orders are saved in memory and committed to db for history only
- 
# Deliverables
- Order book server using gedis2 with SSL support
- Python client for orderbook
- Create a matcher to match selling with buying orders
- Create a trader to actually do the transactions to user wallets

# Design
- API layer accessible through gedis2 server
- SAL layer for handling logic (called by API)
- Matcher
- Trader

# Code
[Order book](https://github.com/rivine/recordchain/tree/master/JumpScale9RecordChain/servers/orderbook)

