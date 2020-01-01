#! /usr/bin/python3
import os
os.chdir('') # Put your working directory
import rest_api as api
from time import sleep
from telegram_bot import *
import logging
logger=logging.getLogger()
logger.handlers = []
logging.basicConfig(filename=f"{os.getcwd()}/real_bot_telegram.log",format='%(asctime)s - %(process)d-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

# --------------------------


def update(bot):
    while True:
        try:
            bot.update_position()
            logging.info('update_position')
        except:
            logging.info('update_position failed')
        sleep(15*60)
