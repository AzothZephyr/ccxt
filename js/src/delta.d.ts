import Exchange from './abstract/delta.js';
import { Balances, Int, OHLCV, Order, OrderBook, OrderSide, OrderType, Ticker, Trade } from './base/types.js';
/**
 * @class delta
 * @extends Exchange
 */
export default class delta extends Exchange {
    describe(): any;
    convertExpireDate(date: any): string;
    createExpiredOptionMarket(symbol: any): {
        id: string;
        symbol: string;
        base: any;
        quote: string;
        settle: string;
        baseId: any;
        quoteId: string;
        settleId: string;
        active: boolean;
        type: string;
        linear: any;
        inverse: any;
        spot: boolean;
        swap: boolean;
        future: boolean;
        option: boolean;
        margin: boolean;
        contract: boolean;
        contractSize: number;
        expiry: number;
        expiryDatetime: string;
        optionType: string;
        strike: number;
        precision: {
            amount: any;
            price: any;
        };
        limits: {
            amount: {
                min: any;
                max: any;
            };
            price: {
                min: any;
                max: any;
            };
            cost: {
                min: any;
                max: any;
            };
        };
        info: any;
    };
    market(symbol: any): any;
    safeMarket(marketId?: any, market?: any, delimiter?: any, marketType?: any): any;
    fetchTime(params?: {}): Promise<number>;
    fetchStatus(params?: {}): Promise<{
        status: string;
        updated: number;
        eta: any;
        url: any;
        info: any;
    }>;
    fetchCurrencies(params?: {}): Promise<{}>;
    loadMarkets(reload?: boolean, params?: {}): Promise<import("./base/types.js").Dictionary<import("./base/types.js").Market>>;
    fetchMarkets(params?: {}): Promise<any[]>;
    parseTicker(ticker: any, market?: any): Ticker;
    fetchTicker(symbol: string, params?: {}): Promise<Ticker>;
    fetchTickers(symbols?: string[], params?: {}): Promise<import("./base/types.js").Dictionary<Ticker>>;
    fetchOrderBook(symbol: string, limit?: Int, params?: {}): Promise<OrderBook>;
    parseTrade(trade: any, market?: any): Trade;
    fetchTrades(symbol: string, since?: Int, limit?: Int, params?: {}): Promise<Trade[]>;
    parseOHLCV(ohlcv: any, market?: any): OHLCV;
    fetchOHLCV(symbol: string, timeframe?: string, since?: Int, limit?: Int, params?: {}): Promise<OHLCV[]>;
    parseBalance(response: any): Balances;
    fetchBalance(params?: {}): Promise<Balances>;
    fetchPosition(symbol: string, params?: {}): Promise<import("./base/types.js").Position>;
    fetchPositions(symbols?: string[], params?: {}): Promise<import("./base/types.js").Position[]>;
    parsePosition(position: any, market?: any): import("./base/types.js").Position;
    parseOrderStatus(status: any): string;
    parseOrder(order: any, market?: any): Order;
    createOrder(symbol: string, type: OrderType, side: OrderSide, amount: any, price?: any, params?: {}): Promise<Order>;
    editOrder(id: string, symbol: any, type: any, side: any, amount?: any, price?: any, params?: {}): Promise<Order>;
    cancelOrder(id: string, symbol?: string, params?: {}): Promise<Order>;
    cancelAllOrders(symbol?: string, params?: {}): Promise<any>;
    fetchOpenOrders(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<Order[]>;
    fetchClosedOrders(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<Order[]>;
    fetchOrdersWithMethod(method: any, symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<Order[]>;
    fetchMyTrades(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<Trade[]>;
    fetchLedger(code?: string, since?: Int, limit?: Int, params?: {}): Promise<any>;
    parseLedgerEntryType(type: any): string;
    parseLedgerEntry(item: any, currency?: any): {
        info: any;
        id: string;
        direction: any;
        account: any;
        referenceId: string;
        referenceAccount: any;
        type: string;
        currency: any;
        amount: number;
        before: number;
        after: number;
        status: string;
        timestamp: number;
        datetime: string;
        fee: any;
    };
    fetchDepositAddress(code: string, params?: {}): Promise<{
        currency: any;
        address: string;
        tag: string;
        network: string;
        info: any;
    }>;
    parseDepositAddress(depositAddress: any, currency?: any): {
        currency: any;
        address: string;
        tag: string;
        network: string;
        info: any;
    };
    fetchFundingRate(symbol: string, params?: {}): Promise<{
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
        nextFundingRate: any;
        nextFundingTimestamp: any;
        nextFundingDatetime: any;
        previousFundingRate: any;
        previousFundingTimestamp: any;
        previousFundingDatetime: any;
    }>;
    fetchFundingRates(symbols?: string[], params?: {}): Promise<any>;
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
        nextFundingRate: any;
        nextFundingTimestamp: any;
        nextFundingDatetime: any;
        previousFundingRate: any;
        previousFundingTimestamp: any;
        previousFundingDatetime: any;
    };
    addMargin(symbol: string, amount: any, params?: {}): Promise<{
        info: any;
        type: any;
        amount: any;
        total: number;
        code: any;
        symbol: any;
        status: any;
    }>;
    reduceMargin(symbol: string, amount: any, params?: {}): Promise<{
        info: any;
        type: any;
        amount: any;
        total: number;
        code: any;
        symbol: any;
        status: any;
    }>;
    modifyMarginHelper(symbol: string, amount: any, type: any, params?: {}): Promise<{
        info: any;
        type: any;
        amount: any;
        total: number;
        code: any;
        symbol: any;
        status: any;
    }>;
    parseMarginModification(data: any, market?: any): {
        info: any;
        type: any;
        amount: any;
        total: number;
        code: any;
        symbol: any;
        status: any;
    };
    fetchOpenInterest(symbol: string, params?: {}): Promise<import("./base/types.js").OpenInterest>;
    parseOpenInterest(interest: any, market?: any): import("./base/types.js").OpenInterest;
    fetchLeverage(symbol: string, params?: {}): Promise<any>;
    setLeverage(leverage: any, symbol?: string, params?: {}): Promise<any>;
    fetchSettlementHistory(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<any>;
    parseSettlement(settlement: any, market: any): {
        info: any;
        symbol: any;
        price: number;
        timestamp: number;
        datetime: string;
    };
    parseSettlements(settlements: any, market: any): any[];
    sign(path: any, api?: string, method?: string, params?: {}, headers?: any, body?: any): {
        url: string;
        method: string;
        body: any;
        headers: any;
    };
    handleErrors(code: any, reason: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): any;
}
