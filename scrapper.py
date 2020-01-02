# encoding: utf-8

import logging
import requests
from utils.get_headers import get_headers
from utils.parse_item import parse_item
from persistence.transactions import TransactionsEngine
from bs4 import BeautifulSoup as bs
import time
import random


class HouseScrapper():
    def __init__(self, log_name, tr_engine: TransactionsEngine, config):
        self.config = config

        self.URL = config['scrap_url']

        self.logger = logging.getLogger(log_name)

        self.tr_engine = tr_engine

    def scrap(self):
        header = get_headers()

        attempt = 0
        document = None
        for attempt in range(5):
            if document is None:
                try:
                    document = requests.get(self.URL, headers=header).text
                except Exception as e:
                    self.logger.error(e)
                    self.logger.debug(f'Error loading webpage. Attempt number {attempt + 1}')
                    time.sleep(random.randrange(3) + 3)

        if document is None:
            self.logger.error("Error loading webpage. Max attempts reached, going to sleep...")
        else:
            web = bs(document, "html.parser")

            last_url = self.tr_engine.get_last_to_check()
            first = True
            last_reached = False
            for link in web.findAll('a', class_="item-link"):
                if not last_reached:
                    item_url = f"{self.config['scrap_url_base']}{link['href']}"

                    self.logger.debug(f'Parsing {item_url}')

                    if last_url is not None and item_url == last_url:
                        last_reached = True
                        self.logger.info("Last item reached, going to sleep...")
                    else:
                        date = parse_item(item_url, self.logger)

                        self.tr_engine.insert_item(item_url, date)

                        time.sleep(5)

                        if first:
                            first = False
                            self.tr_engine.update_last_to_check(str(item_url))
        return 0