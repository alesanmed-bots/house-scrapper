# encoding: utf-8

import logging
import sqlite3
import datetime
from os import path

class TransactionsEngine():
    def __init__(self, db_name, log_name):
        self.db_name = db_name

        self.log = logging.getLogger(log_name)

        self.connect()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS last_item (url text primary key)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS items (url text primary key, date text, price integer,
                            more_info text, timestamp datetime DEFAULT CURRENT_TIMESTAMP, 
                            fetched integer DEFAULT 0)''')

        self.conn.commit()

    def connect(self):
        self.conn = sqlite3.connect(path.abspath(path.join(path.dirname(__file__), f'files/{self.db_name}')))

        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def get_last_to_check(self):
        self.cursor.execute("""SELECT * FROM last_item""")

        item = self.cursor.fetchone()

        if item is None:
            return item
        else:
            return item[0]


    def update_last_to_check(self, last_url):
        self.cursor.execute("""SELECT COUNT(*) from last_item""")

        count = self.cursor.fetchone()[0]

        if count <= 0:
            self.cursor.execute("""INSERT INTO last_item VALUES (?)""", (last_url,))
        else:
            self.cursor.execute("""UPDATE last_item SET url = ?""", (last_url,))

        conn.commit()


    def insert_item(self, url, date, price, more_info):
        try:
            self.cursor.execute("""INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)""",
                        (url, date, price, more_info, datetime.datetime.now(), 0))

            conn.commit()
        except sqlite3.DatabaseError as exception:
            self.log.warning('item {} not inserted due to: {}'.format(url, str(exception)))


    def set_item_fetched(self, url):
        self.cursor.execute(
            """UPDATE items SET fetched = 1 WHERE url = ?""", (url,))

        conn.commit()


    def get_unfetched_items(self):
        self.cursor.execute("""SELECT * FROM items WHERE fetched = 0 ORDER BY timestamp DESC""")

        items = self.cursor.fetchall()

        return items
