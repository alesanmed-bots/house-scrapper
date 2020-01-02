# coding: utf-8
import signal
import sys
import os

import conf
from conf import logger
from persistence.transactions import TransactionsEngine
from scrapper import HouseScrapper

def graceful_exit(*args, **kwargs):
    """Provide a graceful exit from a webhook server."""
    if tr_engine is not None:
        tr_engine.disconnect()

    sys.exit(1)

if __name__ == "__main__":
    global tr_engine

    config = conf.get_config()

    tr_engine = TransactionsEngine(config['db_name'], config['log_name'])

    house_scrapper = HouseScrapper(config['log_name'], tr_engine, config)

    signal.signal(signal.SIGINT, graceful_exit)

    house_scrapper.scrap()

    tr_engine.disconnect()
