#! /usr/bin/python3
# longandshort.io
# Implementation of https://github.com/bybit-exchange/bybit-official-api-docs/blob/master/en/README.md
import requests
import os
import websocket,time
import hmac
import hashlib
import json
import logging
logger=logging.getLogger()
logger.handlers = []
logging.basicConfig(filename=f"{os.getcwd()}/rest_api.log",format='%(asctime)s - %(process)d-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

class Account:
    def __init__(self, api_key, secret, leverage, url="https://api.bybit.com"):
        """Use https://api.bybit.com if you do not want to use the Testnet"""
        self.api_key=api_key
        self.secret = secret
        self.leverage=leverage
        self.url=url
        logging.info(f'Bybit session initiated : API Key : {self.api_key}, Leverage : {self.leverage}, URL : {self.url}')

    def get_signature(self,param_str):
        return str(hmac.new(bytes(self.secret, "utf-8"), bytes(param_str, "utf-8"), digestmod="sha256").hexdigest())

    def auth(self):
        logger.info("auth")
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('auth')
        r = requests.post(self.url+'/user/leverage/save', data)
        logging.info(r.text)
        return json.loads(r.text)

    def place_active_order(self, side,  qty, price,stop_loss,take_profit,order_type="Limit",time_in_force='GoodTillCancel'):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&order_type={order_type}&price={price}&qty={qty}&side={side}&stop_loss={stop_loss}&symbol=BTCUSD&take_profit={take_profit}&time_in_force={time_in_force}&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "timestamp":timestamp,

            "side":side,
            "symbol":"BTCUSD",
            "order_type":order_type,
            "qty":qty,
            "price": price,
            "time_in_force":time_in_force,
            "take_profit":take_profit,
            "stop_loss": stop_loss,
            "sign":sign
            }
        logging.info('place_active_order')
        r=requests.post(self.url+'/open-api/order/create',data)
        logging.info(r.text)
        return json.loads(r.text)

    def market_close(self, side,  qty, price="",order_type="Market",time_in_force=''):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&order_type={order_type}&price={price}&qty={qty}&side={side}&symbol=BTCUSD&time_in_force={time_in_force}&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "timestamp":timestamp,

            "side":side,
            "symbol":"BTCUSD",
            "order_type":order_type,
            "qty":qty,
            "price": price,
            "time_in_force":time_in_force,
            "sign":sign
            }
        logging.info('market_close')
        r=requests.post(self.url+'/open-api/order/create',data)
        logging.info(r.text)
        return json.loads(r.text)


    def get_active_order(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_active_order')
        r=requests.get(self.url+'/open-api/order/list',data)
        logging.info(r.text)
        return json.loads(r.text)

    def cancel_active_order(self, order_id):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&order_id={order_id}&symbol=BTCUSD&timestamp={timestamp}"
        sign=str(hmac.new(bytes(self.secret, "utf-8"), bytes(param_str, "utf-8"), digestmod="sha256").hexdigest())
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign,
            "order_id":order_id
            }
        logging.info('cancel_active_order')
        r=requests.post(self.url+'/open-api/order/cancel',data)
        logging.info(r.text)
        return json.loads(r.text)


    def change_leverage(self, leverage,symbol="BTCUSD"):
        timestamp=int(time.time() * 1000)
        self.leverage=leverage
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":symbol,
            "leverage":self.leverage,
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('change_leverage')
        r=requests.post(self.url+'/user/leverage/save',data)
        logging.info(r.text)
        return json.loads(r.text)

    def my_position(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('my_position')
        r=requests.get(self.url+'/position/list',data)
        logging.info(r.text)
        return json.loads(r.text)




    def ticker(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info("ticker")
        r=requests.get(self.url+'/v2/public/tickers',data)
        logging.info(r.text)
        return json.loads(r.text)


    def get_orderbook(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_orderbook')
        r=requests.get(self.url+'/v2/public/tickers',data)
        logging.info(r.text)
        return json.loads(r.text)

    def replace_order(self, order_id):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&leverage={self.leverage}&order_id={order_id}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "leverage":self.leverage,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            'order_id': order_id,
            "sign":sign
            }
        logging.info('replace_order')
        r=requests.post(self.url+'/open-api/order/replace',data)
        logging.info(r.text)
        return json.loads(r.text)

    def get_leverage(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_leverage')
        r=requests.get(self.url+'/user/leverage',data)
        logging.info(r.text)
        return json.loads(r.text)

    def get_wallet_fund_records(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_waller_fund_records')
        r=requests.get(self.url+'/open-api/wallet/fund/records',data)
        logging.info(r.text)
        return json.loads(r.text)

    def get_withdraw_records(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_withdraw_records')
        r=requests.get(self.url+'/open-api/wallet/withdraw/list',data)
        logging.info(r.text)
        return json.loads(r.text)

    def get_the_last_funding_rate(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_the_last_funding_rate')
        r=requests.get(self.url+'/open-api/funding/prev-funding-rate',data)
        logging.info(r.text)
        return json.loads(r.text)

    def get_my_last_funding_fee(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info("get_my_last_funding_fee")
        r=requests.get(self.url+'/open-api/funding/prev-funding',data)
        logging.info(r.text)
        return json.loads(r.text)

    def get_predicted_funding_rate_funding_fee(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_predicted_funding_rate_funding_fee')
        r=requests.get(self.url+'/open-api/funding/predicted-funding',data)
        logging.info(r.text)
        return json.loads(r.text)

    def get_trade_records(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_trade_records')
        r=requests.get(self.url+'/v2/private/execution/list',data)
        logging.info(r.text)
        return json.loads(r.text)

    def latest_info_btc(self):
        timestamp=int(time.time() * 1000)
        param_str = f"api_key={self.api_key}&symbol=BTCUSD&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":"BTCUSD",
            "timestamp":timestamp,
            "sign":sign
            }
        logging.info('get_last_info_btc')
        r=requests.get(self.url+'/v2/public/tickers',data)
        logging.info(r.text)
        return json.loads(r.text)

    def cancel_all_pending_order(self):
        try:
            liste=self.get_active_order()['result']['data']
            for x in liste:
                if x['order_status']=='New':
                    self.cancel_active_order(x['order_id'])
        except:
            pass

    def get_kline(self, symbol="BTCUSD", interval=360, limit=200):
        timestamp=int(time.time() * 1000)
        if interval=="D":
            _from=int(time.time()-1440*60*limit)
        else:
            _from=int(time.time()-60*interval*limit)
        param_str = f"api_key={self.api_key}&symbol={symbol}&interval={interval}&from={_from}&limit={limit}&timestamp={timestamp}"
        sign=self.get_signature(param_str)
        data={
            "api_key":self.api_key,
            "symbol":symbol,
            "timestamp":timestamp,
            "interval": interval,
            "from":_from,
            "limit": limit,
            "sign":sign
            }
        logging.info('get_kline')
        r=requests.get(self.url+'/v2/public/kline/list',data)
        logging.info(r.text)
        return json.loads(r.text)
