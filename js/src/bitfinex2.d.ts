import Exchange from './abstract/bitfinex2.js';
import { Int, OrderSide, OrderType, Trade, OHLCV, Order, FundingRateHistory, OrderBook, Transaction, Ticker } from './base/types.js';
/**
 * @class bitfinex2
 * @extends Exchange
 */
export default class bitfinex2 extends Exchange {
    describe(): any;
    isFiat(code: any): boolean;
    getCurrencyId(code: any): string;
    getCurrencyName(code: any): any;
    amountToPrecision(symbol: any, amount: any): any;
    priceToPrecision(symbol: any, price: any): any;
    fetchStatus(params?: {}): Promise<{
        status: string;
        updated: any;
        eta: any;
        url: any;
        info: any;
    }>;
    fetchMarkets(params?: {}): Promise<any[]>;
    fetchCurrencies(params?: {}): Promise<{}>;
    safeNetwork(networkId: any): string;
    fetchBalance(params?: {}): Promise<import("./base/types.js").Balances>;
    transfer(code: string, amount: any, fromAccount: any, toAccount: any, params?: {}): Promise<{
        id: any;
        timestamp: number;
        datetime: string;
        status: string;
        amount: number;
        currency: any;
        fromAccount: string;
        toAccount: string;
        info: any;
    }>;
    parseTransfer(transfer: any, currency?: any): {
        id: any;
        timestamp: number;
        datetime: string;
        status: string;
        amount: number;
        currency: any;
        fromAccount: string;
        toAccount: string;
        info: any;
    };
    parseTransferStatus(status: any): string;
    convertDerivativesId(currency: any, type: any): any;
    fetchOrderBook(symbol: string, limit?: Int, params?: {}): Promise<OrderBook>;
    parseTicker(ticker: any, market?: any): Ticker;
    fetchTickers(symbols?: string[], params?: {}): Promise<import("./base/types.js").Dictionary<Ticker>>;
    fetchTicker(symbol: string, params?: {}): Promise<Ticker>;
    parseTrade(trade: any, market?: any): Trade;
    fetchTrades(symbol: string, since?: Int, limit?: Int, params?: {}): Promise<Trade[]>;
    fetchOHLCV(symbol: string, timeframe?: string, since?: Int, limit?: number, params?: {}): Promise<OHLCV[]>;
    parseOHLCV(ohlcv: any, market?: any): OHLCV;
    parseOrderStatus(status: any): any;
    parseOrderFlags(flags: any): any;
    parseTimeInForce(orderType: any): string;
    parseOrder(order: any, market?: any): Order;
    createOrder(symbol: string, type: OrderType, side: OrderSide, amount: any, price?: any, params?: {}): Promise<Order>;
    cancelAllOrders(symbol?: string, params?: {}): Promise<Order[]>;
    cancelOrder(id: string, symbol?: string, params?: {}): Promise<Order>;
    fetchOpenOrder(id: string, symbol?: string, params?: {}): Promise<any>;
    fetchClosedOrder(id: string, symbol?: string, params?: {}): Promise<any>;
    fetchOpenOrders(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<Order[]>;
    fetchClosedOrders(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<Order[]>;
    fetchOrderTrades(id: string, symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<Trade[]>;
    fetchMyTrades(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<Trade[]>;
    createDepositAddress(code: string, params?: {}): Promise<{
        currency: string;
        address: string;
        tag: string;
        network: any;
        info: any;
    }>;
    fetchDepositAddress(code: string, params?: {}): Promise<{
        currency: string;
        address: string;
        tag: string;
        network: any;
        info: any;
    }>;
    parseTransactionStatus(status: any): string;
    parseTransaction(transaction: any, currency?: any): Transaction;
    fetchTradingFees(params?: {}): Promise<{}>;
    fetchDepositsWithdrawals(code?: string, since?: Int, limit?: Int, params?: {}): Promise<any>;
    withdraw(code: string, amount: any, address: any, tag?: any, params?: {}): Promise<any>;
    fetchPositions(symbols?: string[], params?: {}): Promise<import("./base/types.js").Position[]>;
    parsePosition(position: any, market?: any): import("./base/types.js").Position;
    nonce(): number;
    sign(path: any, api?: string, method?: string, params?: {}, headers?: any, body?: any): {
        url: string;
        method: string;
        body: any;
        headers: any;
    };
    handleErrors(statusCode: any, statusText: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): any;
    parseLedgerEntryType(type: any): any;
    parseLedgerEntry(item: any, currency?: any): {
        id: string;
        direction: any;
        account: any;
        referenceId: string;
        referenceAccount: any;
        type: any;
        currency: any;
        amount: number;
        timestamp: number;
        datetime: string;
        before: any;
        after: number;
        status: any;
        fee: any;
        info: any;
    };
    fetchLedger(code?: string, since?: Int, limit?: Int, params?: {}): Promise<any>;
    fetchFundingRate(symbol: string, params?: {}): Promise<{}>;
    fetchFundingRates(symbols?: string[], params?: {}): Promise<{}>;
    fetchFundingRateHistory(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<FundingRateHistory[]>;
    parseFundingRate(contract: any, market?: any): {
        info: any;
        symbol: any;
        markPrice: number;
        indexPrice: number;
        interestRate: any;
        estimatedSettlePrice: any;
        timestamp: number;
        datetime: string;
        fundingRate: number;
        fundingTimestamp: any;
        fundingDatetime: any;
        nextFundingRate: number;
        nextFundingTimestamp: number;
        nextFundingDatetime: string;
        previousFundingRate: any;
        previousFundingTimestamp: any;
        previousFundingDatetime: any;
    };
    parseFundingRateHistory(contract: any, market?: any): {
        info: any;
        symbol: any;
        markPrice: number;
        indexPrice: number;
        interestRate: any;
        estimatedSettlePrice: any;
        timestamp: number;
        datetime: string;
        fundingRate: number;
        fundingTimestamp: any;
        fundingDatetime: any;
        nextFundingRate: number;
        nextFundingTimestamp: number;
        nextFundingDatetime: string;
        previousFundingRate: any;
        previousFundingTimestamp: any;
        previousFundingDatetime: any;
    };
}
