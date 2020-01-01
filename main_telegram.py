#! /usr/bin/python3
import os
os.chdir('') # Put your working directory
from real_bot_telegram import *
import threading
import rest_api as api
# ------- Bybit session
api_key="" # API key
secret="" # Private key
leverage=1 # Leverage
session=api.Account(api_key,secret,leverage)
# ------- Telegram bot
token="" # Enter your Telegram Token
chat_id="" # Enter your Telegra chat ID
bot=TelegramBot(session,token,chat_id)
# -------


if __name__ == '__main__':
    telegram_update = threading.Thread(target=update, args=(bot,))
    telegram_update.start()
