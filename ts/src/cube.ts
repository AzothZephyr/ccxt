import Exchange from './abstract/cube.js';

/**
 * @class cube
 * @extends Exchange
 */
export default class cube extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'cube',
            'name': 'Cube Exchange',
            'countries': [ 'AU', 'PL' ], // TODO
            'version': 'v1',
            // 'rateLimit': 100,
            'pro': false, // TODO
            'has': {
                'CORS': undefined,
                'spot': true,
                'margin': false,
                'swap': false,
                'future': false,
                'option': false,
                'cancelAllOrders': false, // TODO
                'cancelOrder': true, // TODO
                'cancelOrders': false,
                'createOrder': true, // TODO
                'editOrder': false,
                'fetchBalance': true, // TODO
                'fetchBorrowRate': false,
                'fetchBorrowRateHistories': false,
                'fetchBorrowRateHistory': false,
                'fetchBorrowRates': false,
                'fetchClosedOrders': false,
                'fetchCurrencies': false,
                'fetchDepositAddress': false,
                'fetchDeposits': false,
                'fetchFundingHistory': false,
                'fetchFundingRate': false,
                'fetchFundingRateHistory': false,
                'fetchFundingRates': false,
                'fetchIndexOHLCV': false,
                'fetchMarginMode': false,
                'fetchMarkets': true, // TODO
                'fetchMarkOHLCV': false,
                'fetchMyTrades': true, // TODO
                'fetchOHLCV': true, // TODO
                'fetchOpenInterestHistory': false,
                'fetchOpenOrders': true, // TODO
                'fetchOrder': true, // TODO
                'fetchOrderBook': true, // todo
                'fetchOrders': false,
                'fetchOrderTrades': true, // TODO
                'fetchPositionMode': false,
                'fetchPositions': false,
                'fetchPremiumIndexOHLCV': false,
                'fetchTicker': true, // TODO
                'fetchTickers': true, // TODO
                'fetchTime': false,
                'fetchTrades': false,
                'fetchTradingFee': false,
                'fetchTradingFees': false,
                'fetchTransactionFees': false,
                'fetchTransactions': false,
                'fetchTransfer': false,
                'fetchTransfers': false,
                'fetchWithdrawal': false,
                'fetchWithdrawals': false,
                'setLeverage': false,
                'setMarginMode': false,
                'transfer': false,
                'withdraw': false,
                'ws': false,
            },
            'timeframes': {
                '1m': 1,
                '5m': 5,
                '10m': 10,
                '30m': 10,
                '1h': 60,
                '2h': 120,
                '4h': 240,
                '8h': 480,
                '12h': 720,
                '1d': 24,
                '1w': 70,
                '1M': 31,
            },
            'urls': {
                'logo': 'https://avatars.githubusercontent.com/u/128435657?s=200&v=4',
                'api': {
                    'http': 'https://cube.exchange',
                    'ws': 'ws://cube.exchange',
                },
                'www': 'https://cube.exchange/',
                'doc': [
                    'https://cube.exchange/docs',
                ],
                'fees': 'https://helpcenter.ace.io/hc/zh-tw/articles/360018609132-%E8%B2%BB%E7%8E%87%E8%AA%AA%E6%98%8E',
            },
            'requiredCredentials': {
                'apiKey': true,
                'secret': true,
            },
            'api': {
                'public': {
                    'get': [
                        '/ir/v0/markets',
                    ],
                },
                'private': {
                    'post': [
                    ],
                },
            },
            'fees': {
                'trading': {
                    'percentage': true,
                    'maker': this.parseNumber ('0.0'),
                    'taker': this.parseNumber ('0.0'),
                },
            },
            'options': {
                'brokerId': 'ccxt',
            },
            'commonCurrencies': {
            },
        });
    }
}
