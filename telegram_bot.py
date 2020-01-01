import requests
from math import floor

class TelegramBot:

    def __init__(self, bybit_session, token, chat_id):

        self.token=token # Token
        self.telegram_url = 'https://api.telegram.org/bot{}'.format(self.token)
        self.chat_id = chat_id
        self.send_url = self.telegram_url + '/sendMessage?chat_id={}&text={}'
        self.session = bybit_session


    def send_message(self,text):

        res = requests.get(self.send_url.format(self.chat_id, text))

        return True if res.status_code == 200 else False

    def update_position(self):
        my_position=self.session.my_position()['result'][0]
        side=my_position['side']
        funding_rate=self.session.get_the_last_funding_rate()["result"]["funding_rate"]
        predicted_funding_rate=self.session.get_predicted_funding_rate_funding_fee()["result"]["predicted_funding_rate"]
        size=my_position['size']
        unrealised_pnl=my_position['unrealised_pnl']*float(self.session.get_orderbook()['result'][0]['last_price'])
        entry_price=my_position['entry_price']
        stop_loss=my_position['stop_loss']
        take_profit=my_position['take_profit']
        liq_price=my_position['liq_price']
        if side!="None":
            self.send_message("Long&Short.io - WaveTrend Strategy - Bybit:")
            message=f"Side = {side}, Size = {size}, PnL = ${round(unrealised_pnl,2)}, Entry Price = {round(entry_price,2)}, Stop Loss = {stop_loss}, Take Profit = {take_profit}, Liq Price = {liq_price}, Funding rate = {funding_rate}, Predicted funding rate = {predicted_funding_rate}"
            self.send_message(message)
