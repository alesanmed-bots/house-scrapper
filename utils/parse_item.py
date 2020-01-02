# encoding: utf-8

from bs4 import BeautifulSoup as bs
import requests
import logging
from utils.user_agent import get_user_agent
import time
import random
import re


def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def parse_item(item_url, logger):
    item_date = None

    if type(item_url) != str:
        raise ValueError("item_url is not a String object")

    header = {'user-agent': get_user_agent()}

    attempt = 0
    document = None

    for attempt in range(5):
        try:
            document = requests.get(item_url, headers=header).text
            break
        except Exception as e:
            logger.error(e)
            logger.debug("Error loading item page. Attempt number {0}".format(attempt + 1))
            time.sleep(random.randrange(3) + 3)

    if attempt >= 4:
        logger.error("Error loading item page. Max attempts reached, returning...")
    else:
        item_page = bs(document, 'html.parser')

        content = item_page.find(
            "span",
            class_="main-info__title-main")

        for p in content:
            if p.find(text=re.compile("Fechas")):
                item_date = p.text.split("Fechas:")[-1].strip()

                break

    return item_date
