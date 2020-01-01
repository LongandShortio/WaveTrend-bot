#! /usr/bin/python3
import os
os.chdir('') # Put your working directory
import rest_api as api
from time import sleep
from math import floor
import indicators
import pandas as pd
from telegram_bot import *
import logging
logger=logging.getLogger()
logger.handlers = []
logging.basicConfig(filename=f"{os.getcwd()}/real_bot.log",format='%(asctime)s - %(process)d-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

# --------------------------



def long(diff,e=0):
    if diff.iloc[-1]>e and diff.iloc[-2]<e: return True

    return False

def short(diff,e=-0):
    if diff.iloc[-1]<e and diff.iloc[-2]>e: return True
    return False


def trading(session, bot):
    timeframe="D" # Looking at the daily timeframe
    logging.info('+++++++++++++++ Start trading +++++++++++++++')
    while True:

        logging.info('+++++++++++++++ Get data +++++++++++++++')
        kline=session.get_kline(interval=timeframe)
        data={'close': [float(x["close"]) for x in kline["result"]],
            'open': [float(x["open"]) for x in kline["result"]],
            'high':[float(x["high"]) for x in kline["result"]] ,
            'low': [float(x["low"]) for x in kline["result"]],
            }
        df=pd.DataFrame(data=data)

        del data

        diff=indicators.wave_trend(df)
        diff=diff.reset_index().drop('index',axis=1)

        go_long, go_short=long(diff['diff']), short(diff['diff'])
        logging.info("+++++++++++++++ Go long +++++++++++++++")
        logging.info(go_long)
        logging.info("+++++++++++++++ Go short +++++++++++++++")
        logging.info(go_short)
        logging.info("+++++++++++++++ Shows the tail +++++++++++++++")
        logging.info(diff.tail())

        del diff
        try:
            my_position= session.my_position()['result'][0]['side']
            logging.info('+++++++++++++++ Position obtained +++++++++++++++')


            if my_position=="None" and go_long:
                logging.info('+++++++++++++++ my_position==None and go_long +++++++++++++++')
                session.cancel_all_pending_order()
                price=floor(float(session.get_orderbook()['result'][0]['ask_price'])-20)
                stop_loss=floor(float(price*0.90)) # SL @ 10%
                take_profit=floor(float(price*1.5)) # TP @ 50 %
                wallet_balance=session.my_position()['result'][0]['wallet_balance']
                leverage=session.my_position()['result'][0]['leverage']
                size=500 # Choose the size of your position
                session.place_active_order("Buy", size, price, stop_loss, take_profit)
                bot.send_message("Had no position and placed long order")
                message=f"Price = {price}, Size = {size}, Leverage = {leverage}, Stop Loss = {stop_loss}, Take Profit = {take_profit}"
                bot.send_message(message)
                sleep(30*60)
                logging.info('+++++++++++++++ Sleep 5*60s for the order to get filled +++++++++++++++')

            elif my_position=="None" and go_short:
                session.cancel_all_pending_order()
                logging.info('+++++++++++++++ my_position==None and go_short +++++++++++++++')
                price=floor(float(session.get_orderbook()['result'][0]['bid_price'])+20)
                stop_loss=floor(float(price*1.10)) # SL @ 10%
                take_profit=floor(float(price*0.50)) # TP @ 50 %
                wallet_balance=session.my_position()['result'][0]['wallet_balance']
                leverage=session.my_position()['result'][0]['leverage']
                size=500 # Choose the size of your position
                session.place_active_order("Sell", size, price, stop_loss, take_profit)
                bot.send_message("Had no position and placed short order")
                message=f"Price = {price}, Size = {size}, Leverage = {leverage}, Stop Loss = {stop_loss}, Take Profit = {take_profit}"
                bot.send_message(message)
                sleep(30*60)
                logging.info('+++++++++++++++ Sleep for the order to get filled +++++++++++++++')

            elif my_position=="Sell" and go_long:
                session.cancel_all_pending_order()
                logging.info('+++++++++++++++ my_position==Sell and go_long +++++++++++++++')
                size=session.my_position()['result'][0]['size']
                session.market_close("Buy", size)

                price=floor(float(session.get_orderbook()['result'][0]['ask_price'])-20) #2
                stop_loss=floor(float(price*0.90)) # SL @ 10%
                take_profit=floor(float(price*1.50)) # TP @ 50 %
                wallet_balance=session.my_position()['result'][0]['wallet_balance']
                leverage=session.my_position()['result'][0]['leverage']
                size=500 # Choose the size of your position
                session.place_active_order("Buy", size, price, stop_loss, take_profit)
                bot.send_message("Just closed a short and placed long order")
                message=f"Price = {price}, Size = {size}, Leverage = {leverage}, Stop Loss = {stop_loss}, Take Profit = {take_profit}"
                bot.send_message(message)
                sleep(30*60)
                logging.info('+++++++++++++++ Sleep for the order to get filled +++++++++++++++')

            elif my_position=="Buy" and go_short:
                session.cancel_all_pending_order()
                logging.info('+++++++++++++++ my_position==Buy and go_short +++++++++++++++')
                size=session.my_position()['result'][0]['size']
                session.market_close("Sell", size)

                price=floor(float(session.get_orderbook()['result'][0]['bid_price'])+20) #2
                stop_loss=floor(float(price*1.10)) # SL @ 10%
                take_profit=floor(float(price*0.50)) # TP @ 50 %
                wallet_balance=session.my_position()['result'][0]['wallet_balance']
                leverage=session.my_position()['result'][0]['leverage']
                size=500 # Choose the size of your position
                session.place_active_order("Sell", size, price, stop_loss, take_profit)
                bot.send_message("Just closed a long and placed short order")
                message=f"Price = {price}, Size = {size}, Leverage = {leverage}, Stop Loss = {stop_loss}, Take Profit = {take_profit}"
                bot.send_message(message)
                sleep(30*60)
                logging.info('+++++++++++++++ Sleep for the order to get filled +++++++++++++++')



            logging.info('+++++++++++++++ Sleep 30*60s +++++++++++++++')
            sleep(15*60)
            logging.info('+++++++++++++++ Starts again +++++++++++++++')
        except:
            logging.info('+++++++++++++++ Error getting position +++++++++++++++')
            logging.info('+++++++++++++++ Sleep 10s +++++++++++++++')
            bot.send_message("An error just happenned")
            sleep(10)
