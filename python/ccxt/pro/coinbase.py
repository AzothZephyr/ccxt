# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCacheBySymbolById
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired


class coinbase(ccxt.async_support.coinbase):

    def describe(self):
        return self.deep_extend(super(coinbase, self).describe(), {
            'has': {
                'ws': True,
                'watchOHLCV': False,
                'watchOrderBook': True,
                'watchTicker': True,
                'watchTickers': True,
                'watchTrades': True,
                'watchBalance': False,
                'watchOrders': True,
                'watchMyTrades': False,
            },
            'urls': {
                'api': {
                    'ws': 'wss://advanced-trade-ws.coinbase.com',
                },
            },
            'options': {
                'tradesLimit': 1000,
                'ordersLimit': 1000,
                'myTradesLimit': 1000,
                'sides': {
                    'bid': 'bids',
                    'offer': 'asks',
                },
            },
        })

    async def subscribe(self, name, symbol=None, params={}):
        """
         * @ignore
        subscribes to a websocket channel
        :see: https://docs.cloud.coinbase.com/advanced-trade-api/docs/ws-overview#subscribe
        :param str name: the name of the channel
        :param string|str[] [symbol]: unified market symbol
        :param dict [params]: extra parameters specific to the cex api endpoint
        :returns dict: subscription to a websocket channel
        """
        await self.load_markets()
        self.check_required_credentials()
        market = None
        messageHash = name
        productIds = []
        if isinstance(symbol, list):
            symbols = self.market_symbols(symbol)
            marketIds = self.market_ids(symbols)
            productIds = marketIds
            messageHash = messageHash + '::' + ','.join(symbol)
        elif symbol is not None:
            market = self.market(symbol)
            messageHash = name + '::' + market['id']
            productIds = [market['id']]
        url = self.urls['api']['ws']
        timestamp = self.number_to_string(self.seconds())
        auth = timestamp + name + ','.join(productIds)
        subscribe = {
            'type': 'subscribe',
            'product_ids': productIds,
            'channel': name,
            'api_key': self.apiKey,
            'timestamp': timestamp,
            'signature': self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha256),
        }
        return await self.watch(url, messageHash, subscribe, messageHash)

    async def watch_ticker(self, symbol, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :see: https://docs.cloud.coinbase.com/advanced-trade-api/docs/ws-channels#ticker-channel
        :param str [symbol]: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the coinbasepro api endpoint
        :returns dict: a `ticker structure <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        name = 'ticker'
        return await self.subscribe(name, symbol, params)

    async def watch_tickers(self, symbols=None, params={}):
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :see: https://docs.cloud.coinbase.com/advanced-trade-api/docs/ws-channels#ticker-batch-channel
        :param str[] [symbols]: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the coinbasepro api endpoint
        :returns dict: a `ticker structure <https://github.com/ccxt/ccxt/wiki/Manual#ticker-structure>`
        """
        if symbols is None:
            raise ArgumentsRequired(self.id + ' watchTickers requires a symbols argument')
        name = 'ticker_batch'
        tickers = await self.subscribe(name, symbols, params)
        return tickers

    def handle_tickers(self, client, message):
        #
        #    {
        #        "channel": "ticker",
        #        "client_id": "",
        #        "timestamp": "2023-02-09T20:30:37.167359596Z",
        #        "sequence_num": 0,
        #        "events": [
        #            {
        #                "type": "snapshot",
        #                "tickers": [
        #                    {
        #                        "type": "ticker",
        #                        "product_id": "BTC-USD",
        #                        "price": "21932.98",
        #                        "volume_24_h": "16038.28770938",
        #                        "low_24_h": "21835.29",
        #                        "high_24_h": "23011.18",
        #                        "low_52_w": "15460",
        #                        "high_52_w": "48240",
        #                        "price_percent_chg_24_h": "-4.15775596190603"
        #                    }
        #                ]
        #            }
        #        ]
        #    }
        #
        #    {
        #        "channel": "ticker_batch",
        #        "client_id": "",
        #        "timestamp": "2023-03-01T12:15:18.382173051Z",
        #        "sequence_num": 0,
        #        "events": [
        #            {
        #                "type": "snapshot",
        #                "tickers": [
        #                    {
        #                        "type": "ticker",
        #                        "product_id": "DOGE-USD",
        #                        "price": "0.08212",
        #                        "volume_24_h": "242556423.3",
        #                        "low_24_h": "0.07989",
        #                        "high_24_h": "0.08308",
        #                        "low_52_w": "0.04908",
        #                        "high_52_w": "0.1801",
        #                        "price_percent_chg_24_h": "0.50177456859626"
        #                    }
        #                ]
        #            }
        #        ]
        #    }
        #
        channel = self.safe_string(message, 'channel')
        events = self.safe_value(message, 'events', [])
        newTickers = []
        for i in range(0, len(events)):
            tickersObj = events[i]
            tickers = self.safe_value(tickersObj, 'tickers', [])
            for j in range(0, len(tickers)):
                ticker = tickers[j]
                result = self.parse_ws_ticker(ticker)
                symbol = result['symbol']
                self.tickers[symbol] = result
                wsMarketId = self.safe_string(ticker, 'product_id')
                messageHash = channel + '::' + wsMarketId
                newTickers.append(result)
                client.resolve(result, messageHash)
        messageHashes = self.find_message_hashes(client, 'ticker_batch::')
        for i in range(0, len(messageHashes)):
            messageHash = messageHashes[i]
            parts = messageHash.split('::')
            symbolsString = parts[1]
            symbols = symbolsString.split(',')
            tickers = self.filter_by_array(newTickers, 'symbol', symbols)
            if not self.is_empty(tickers):
                client.resolve(tickers, messageHash)
        return message

    def parse_ws_ticker(self, ticker, market=None):
        #
        #     {
        #         "type": "ticker",
        #         "product_id": "DOGE-USD",
        #         "price": "0.08212",
        #         "volume_24_h": "242556423.3",
        #         "low_24_h": "0.07989",
        #         "high_24_h": "0.08308",
        #         "low_52_w": "0.04908",
        #         "high_52_w": "0.1801",
        #         "price_percent_chg_24_h": "0.50177456859626"
        #     }
        #
        marketId = self.safe_string(ticker, 'product_id')
        timestamp = None
        last = self.safe_number(ticker, 'price')
        return self.safe_ticker({
            'info': ticker,
            'symbol': self.safe_symbol(marketId, market, '-'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high_24_h'),
            'low': self.safe_string(ticker, 'low_24_h'),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': self.safe_string(ticker, 'price_percent_chg_24_h'),
            'average': None,
            'baseVolume': self.safe_string(ticker, 'volume_24_h'),
            'quoteVolume': None,
        })

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :see: https://docs.cloud.coinbase.com/advanced-trade-api/docs/ws-channels#market-trades-channel
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the coinbasepro api endpoint
        :returns dict[]: a list of `trade structures <https://github.com/ccxt/ccxt/wiki/Manual#public-trades>`
        """
        await self.load_markets()
        symbol = self.symbol(symbol)
        name = 'market_trades'
        trades = await self.subscribe(name, symbol, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        watches information on multiple orders made by the user
        :see: https://docs.cloud.coinbase.com/advanced-trade-api/docs/ws-channels#user-channel
        :param str [symbol]: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of  orde structures to retrieve
        :param dict [params]: extra parameters specific to the coinbasepro api endpoint
        :returns dict[]: a list of `order structures <https://github.com/ccxt/ccxt/wiki/Manual#order-structure>`
        """
        await self.load_markets()
        name = 'user'
        orders = await self.subscribe(name, symbol, params)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_since_limit(orders, since, limit, 'timestamp', True)

    async def watch_order_book(self, symbol, limit=None, params={}):
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :see: https://docs.cloud.coinbase.com/advanced-trade-api/docs/ws-channels#level2-channel
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the coinbasepro api endpoint
        :returns dict: A dictionary of `order book structures <https://github.com/ccxt/ccxt/wiki/Manual#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        name = 'level2'
        market = self.market(symbol)
        symbol = market['symbol']
        orderbook = await self.subscribe(name, symbol, params)
        return orderbook.limit()

    def handle_trade(self, client, message):
        #
        #    {
        #        "channel": "market_trades",
        #        "client_id": "",
        #        "timestamp": "2023-02-09T20:19:35.39625135Z",
        #        "sequence_num": 0,
        #        "events": [
        #            {
        #                "type": "snapshot",
        #                "trades": [
        #                    {
        #                        "trade_id": "000000000",
        #                        "product_id": "ETH-USD",
        #                        "price": "1260.01",
        #                        "size": "0.3",
        #                        "side": "BUY",
        #                        "time": "2019-08-14T20:42:27.265Z",
        #                    }
        #                ]
        #            }
        #        ]
        #    }
        #
        events = self.safe_value(message, 'events')
        event = self.safe_value(events, 0)
        trades = self.safe_value(event, 'trades')
        trade = self.safe_value(trades, 0)
        marketId = self.safe_string(trade, 'product_id')
        messageHash = 'market_trades::' + marketId
        symbol = self.safe_symbol(marketId)
        tradesArray = self.safe_value(self.trades, symbol)
        if tradesArray is None:
            tradesLimit = self.safe_integer(self.options, 'tradesLimit', 1000)
            tradesArray = ArrayCacheBySymbolById(tradesLimit)
            self.trades[symbol] = tradesArray
        for i in range(0, len(events)):
            currentEvent = events[i]
            currentTrades = self.safe_value(currentEvent, 'trades')
            for j in range(0, len(currentTrades)):
                item = currentTrades[i]
                tradesArray.append(self.parse_trade(item))
        client.resolve(tradesArray, messageHash)
        return message

    def handle_order(self, client, message):
        #
        #    {
        #        "channel": "user",
        #        "client_id": "",
        #        "timestamp": "2023-02-09T20:33:57.609931463Z",
        #        "sequence_num": 0,
        #        "events": [
        #            {
        #                "type": "snapshot",
        #                "orders": [
        #                    {
        #                        "order_id": "XXX",
        #                        "client_order_id": "YYY",
        #                        "cumulative_quantity": "0",
        #                        "leaves_quantity": "0.000994",
        #                        "avg_price": "0",
        #                        "total_fees": "0",
        #                        "status": "OPEN",
        #                        "product_id": "BTC-USD",
        #                        "creation_time": "2022-12-07T19:42:18.719312Z",
        #                        "order_side": "BUY",
        #                        "order_type": "Limit"
        #                    },
        #                ]
        #            }
        #        ]
        #    }
        #
        events = self.safe_value(message, 'events')
        marketIds = []
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        for i in range(0, len(events)):
            event = events[i]
            responseOrders = self.safe_value(event, 'orders')
            for j in range(0, len(responseOrders)):
                responseOrder = responseOrders[j]
                parsed = self.parse_ws_order(responseOrder)
                cachedOrders = self.orders
                marketId = self.safe_string(responseOrder, 'product_id')
                if not (marketId in marketIds):
                    marketIds.append(marketId)
                cachedOrders.append(parsed)
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            messageHash = 'user::' + marketId
            client.resolve(self.orders, messageHash)
        client.resolve(self.orders, 'user')
        return message

    def parse_ws_order(self, order, market=None):
        #
        #    {
        #        "order_id": "XXX",
        #        "client_order_id": "YYY",
        #        "cumulative_quantity": "0",
        #        "leaves_quantity": "0.000994",
        #        "avg_price": "0",
        #        "total_fees": "0",
        #        "status": "OPEN",
        #        "product_id": "BTC-USD",
        #        "creation_time": "2022-12-07T19:42:18.719312Z",
        #        "order_side": "BUY",
        #        "order_type": "Limit"
        #    }
        #
        id = self.safe_string(order, 'order_id')
        clientOrderId = self.safe_string(order, 'client_order_id')
        marketId = self.safe_string(order, 'product_id')
        datetime = self.safe_string(order, 'time')
        market = self.safe_market(marketId, market)
        return self.safe_order({
            'info': order,
            'symbol': self.safe_string(market, 'symbol'),
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': self.parse8601(datetime),
            'datetime': datetime,
            'lastTradeTimestamp': None,
            'type': self.safe_string(order, 'order_type'),
            'timeInForce': None,
            'postOnly': None,
            'side': self.safe_string(order, 'side'),
            'price': None,
            'stopPrice': None,
            'triggerPrice': None,
            'amount': None,
            'cost': None,
            'average': self.safe_string(order, 'avg_price'),
            'filled': self.safe_string(order, 'cumulative_quantity'),
            'remaining': self.safe_string(order, 'leaves_quantity'),
            'status': self.safe_string_lower(order, 'status'),
            'fee': {
                'amount': self.safe_string(order, 'total_fees'),
                'currency': self.safe_string(market, 'quote'),
            },
            'trades': None,
        })

    def handle_order_book_helper(self, orderbook, updates):
        for i in range(0, len(updates)):
            trade = updates[i]
            sideId = self.safe_string(trade, 'side')
            side = self.safe_string(self.options['sides'], sideId)
            price = self.safe_number(trade, 'price_level')
            amount = self.safe_number(trade, 'new_quantity')
            orderbook[side].store(price, amount)

    def handle_order_book(self, client, message):
        #
        #    {
        #        "channel": "l2_data",
        #        "client_id": "",
        #        "timestamp": "2023-02-09T20:32:50.714964855Z",
        #        "sequence_num": 0,
        #        "events": [
        #            {
        #                "type": "snapshot",
        #                "product_id": "BTC-USD",
        #                "updates": [
        #                    {
        #                        "side": "bid",
        #                        "event_time": "1970-01-01T00:00:00Z",
        #                        "price_level": "21921.73",
        #                        "new_quantity": "0.06317902"
        #                    },
        #                    {
        #                        "side": "bid",
        #                        "event_time": "1970-01-01T00:00:00Z",
        #                        "price_level": "21921.3",
        #                        "new_quantity": "0.02"
        #                    },
        #                ]
        #            }
        #        ]
        #    }
        #
        events = self.safe_value(message, 'events')
        datetime = self.safe_string(message, 'timestamp')
        for i in range(0, len(events)):
            event = events[i]
            updates = self.safe_value(event, 'updates', [])
            marketId = self.safe_string(event, 'product_id')
            messageHash = 'level2::' + marketId
            subscription = self.safe_value(client.subscriptions, messageHash, {})
            limit = self.safe_integer(subscription, 'limit')
            symbol = self.safe_symbol(marketId)
            type = self.safe_string(event, 'type')
            if type == 'snapshot':
                self.orderbooks[symbol] = self.order_book({}, limit)
                orderbook = self.orderbooks[symbol]
                self.handle_order_book_helper(orderbook, updates)
                orderbook['timestamp'] = None
                orderbook['datetime'] = None
                orderbook['symbol'] = symbol
                client.resolve(orderbook, messageHash)
            elif type == 'update':
                orderbook = self.orderbooks[symbol]
                self.handle_order_book_helper(orderbook, updates)
                orderbook['datetime'] = datetime
                orderbook['timestamp'] = self.parse8601(datetime)
                orderbook['symbol'] = symbol
                client.resolve(orderbook, messageHash)
        return message

    def handle_subscription_status(self, client, message):
        #
        #     {
        #         "type": "subscriptions",
        #         "channels": [
        #             {
        #                 "name": "level2",
        #                 "product_ids": ["ETH-BTC"]
        #             }
        #         ]
        #     }
        #
        return message

    def handle_message(self, client, message):
        channel = self.safe_string(message, 'channel')
        methods = {
            'subscriptions': self.handle_subscription_status,
            'ticker': self.handle_tickers,
            'ticker_batch': self.handle_tickers,
            'market_trades': self.handle_trade,
            'user': self.handle_order,
            'l2_data': self.handle_order_book,
        }
        type = self.safe_string(message, 'type')
        if type == 'error':
            errorMessage = self.safe_string(message, 'message')
            raise ExchangeError(errorMessage)
        method = self.safe_value(methods, channel)
        return method(client, message)
