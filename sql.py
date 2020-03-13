# SQLの接続、読み込みなどをする用

import psycopg2


def connect(self):
    self.conn = psycopg2.connect("host=127.0.0.1 dbname=food user=postgres password=8610naka")#ここは変えてください
    self.cur = self.conn.cursor()


def query(self, text):
    self.cur.execute(text)
    return self.cur.fetchone()


def add(self, text):
    self.cur.execute(text)
    self.conn.commit()
