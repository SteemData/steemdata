import time
from decimal import Decimal
from operator import mul
from pprint import pprint
from statistics import mean

import requests
import steem as stm
from funcy.flow import silent
from steem.amount import Amount


class Tickers(object):
    @staticmethod
    def btc_usd_ticker(verbose=False):
        prices = {}
        urls = [
            "https://api.bitfinex.com/v1/pubticker/BTCUSD",
            # "https://api.coinbase.com/v2/prices/BTC-USD/spot",
            "https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
            "https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd",
            "https://www.bitstamp.net/api/v2/ticker/btcusd/",
        ]
        responses = list(silent(requests.get)(u, timeout=30) for u in urls)

        for r in [x for x in responses if hasattr(x, "status_code") and x.status_code == 200 and x.json()]:
            if "bitfinex" in r.url:
                data = r.json()
                prices['bitfinex'] = {'price': float(data['last_price']), 'volume': float(data['volume'])}
            elif "kraken" in r.url:
                data = r.json()['result']['XXBTZUSD']['p']
                prices['kraken'] = {'price': float(data[0]), 'volume': float(data[1])}
            elif "okcoin" in r.url:
                data = r.json()["ticker"]
                prices['okcoin'] = {'price': float(data['last']), 'volume': float(data['vol'])}
            elif "bitstamp" in r.url:
                data = r.json()
                prices['bitstamp'] = {'price': float(data['last']), 'volume': float(data['volume'])}
            elif "btce" in r.url:
                data = r.json()["ticker"]
                prices['btce'] = {'price': float(data['avg']), 'volume': float(data['vol_cur'])}

        if verbose:
            pprint(prices)

        if len(prices) == 0:
            raise RuntimeError("Obtaining BTC/USD prices has failed from all sources.")

        # vwap
        return Tickers._wva(
            [x['price'] for x in prices.values()],
            [x['volume'] for x in prices.values()])

    @staticmethod
    def steem_btc_ticker():
        prices = {}
        urls = [
            "https://poloniex.com/public?command=returnTicker",
            "https://bittrex.com/api/v1.1/public/getmarketsummary?market=BTC-STEEM",
        ]
        responses = list(silent(requests.get)(u, timeout=30) for u in urls)

        for r in [x for x in responses if hasattr(x, "status_code") and x.status_code == 200 and x.json()]:
            if "poloniex" in r.url:
                data = r.json()["BTC_STEEM"]
                prices['poloniex'] = {'price': float(data['last']), 'volume': float(data['baseVolume'])}
            elif "bittrex" in r.url:
                data = r.json()["result"][0]
                price = (data['Bid'] + data['Ask']) / 2
                prices['bittrex'] = {'price': price, 'volume': data['BaseVolume']}

        if len(prices) == 0:
            raise RuntimeError("Obtaining STEEM/BTC prices has failed from all sources.")

        return Tickers._wva(
            [x['price'] for x in prices.values()],
            [x['volume'] for x in prices.values()])

    @staticmethod
    def sbd_btc_ticker(verbose=False):
        prices = {}
        urls = [
            "https://poloniex.com/public?command=returnTicker",
            "https://bittrex.com/api/v1.1/public/getmarketsummary?market=BTC-SBD",
        ]
        responses = list(silent(requests.get)(u, timeout=30) for u in urls)

        for r in [x for x in responses if hasattr(x, "status_code") and x.status_code == 200 and x.json()]:
            if "poloniex" in r.url:
                data = r.json()["BTC_SBD"]
                if verbose:
                    print("Spread on Poloniex is %.2f%%" % Tickers.calc_spread(data['highestBid'], data['lowestAsk']))
                prices['poloniex'] = {'price': float(data['last']), 'volume': float(data['baseVolume'])}
            elif "bittrex" in r.url:
                data = r.json()["result"][0]
                if verbose:
                    print("Spread on Bittrex is %.2f%%" % Tickers.calc_spread(data['Bid'] + data['Ask']))
                price = (data['Bid'] + data['Ask']) / 2
                prices['bittrex'] = {'price': price, 'volume': data['BaseVolume']}

        if len(prices) == 0:
            raise RuntimeError("Obtaining SBD/BTC prices has failed from all sources.")

        return Tickers._wva(
            [x['price'] for x in prices.values()],
            [x['volume'] for x in prices.values()])

    @staticmethod
    def calc_spread(bid, ask):
        return (1 - (Decimal(bid) / Decimal(ask))) * 100

    @staticmethod
    def _wva(values, weights):
        """ Calculates a weighted average
        """
        assert len(values) == len(weights) and len(weights) > 0
        return sum([mul(*x) for x in zip(values, weights)]) / sum(weights)


class Markets(Tickers):
    def __init__(self, cache_timeout=60, steem_instance=None):
        if not steem_instance:
            steem_instance = stm.Steem()
        self.steem = steem_instance

        self._cache_timeout = cache_timeout
        self._cache_timer = time.time()
        self._btc_usd = None
        self._steem_btc = None
        self._sbd_btc = None

    def _has_cache_expired(self):
        if self._cache_timer + self._cache_timeout < time.time():
            self._cache_timer = time.time()
            return True
        return False

    def btc_usd(self):
        if (self._btc_usd is None) or self._has_cache_expired():
            self._btc_usd = self.btc_usd_ticker()
        return self._btc_usd

    def steem_btc(self):
        if (self._steem_btc is None) or self._has_cache_expired():
            self._steem_btc = self.steem_btc_ticker()
        return self._steem_btc

    def sbd_btc(self):
        if (self._sbd_btc is None) or self._has_cache_expired():
            self._sbd_btc = self.sbd_btc_ticker()
        return self._sbd_btc

    def steem_sbd_implied(self):
        return self.steem_btc() / self.sbd_btc()

    def steem_usd_implied(self):
        return self.steem_btc() * self.btc_usd()

    def sbd_usd_implied(self):
        return self.sbd_btc() * self.btc_usd()

    def avg_witness_price(self, take=10):
        price_history = self.steem.get_feed_history()['price_history']
        return mean([Amount(x['base']).amount * Amount(x['quote']).amount for x in price_history[-take:]])
